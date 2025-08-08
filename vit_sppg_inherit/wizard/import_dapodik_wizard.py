# -*- coding: utf-8 -*-

import base64
import csv
import io
import logging
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

try:
    import xlrd
    HAS_XLRD = True
except ImportError:
    HAS_XLRD = False

_logger = logging.getLogger(__name__)

class ImportDapodikWizard(models.TransientModel):
    _name = 'vit.import.dapodik.wizard'
    _description = 'Wizard to Import Dapodik Data'

    file_data = fields.Binary(string='File', required=True)
    file_name = fields.Char(string='File Name')

    def _to_int(self, value):
        """Helper to safely convert string to integer."""
        try:
            return int(float(value)) if value else 0
        except (ValueError, TypeError):
            return 0

    def _to_float(self, value):
        """Helper to safely convert string to float."""
        try:
            return float(value) if value else 0.0
        except (ValueError, TypeError):
            return 0.0

    def _detect_file_type(self, raw_bytes):
        """Detect file type based on file signature"""
        if raw_bytes.startswith(b'PK'):
            return 'xlsx'
        elif raw_bytes.startswith(b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'):
            return 'xls'
        else:
            return 'csv'

    def _read_excel_file(self, raw_bytes, file_type):
        """Read Excel file and convert to list of rows"""
        if file_type == 'xlsx':
            if not HAS_OPENPYXL:
                raise ValidationError(_("openpyxl library is required to read Excel files. Please install it: pip install openpyxl"))
            
            workbook = openpyxl.load_workbook(io.BytesIO(raw_bytes))
            worksheet = workbook.active
            
            rows = []
            for row in worksheet.iter_rows(values_only=True):
                # Convert None values to empty strings
                converted_row = [str(cell) if cell is not None else '' for cell in row]
                rows.append(converted_row)
            
            return rows
            
        elif file_type == 'xls':
            if not HAS_XLRD:
                raise ValidationError(_("xlrd library is required to read Excel files. Please install it: pip install xlrd"))
            
            workbook = xlrd.open_workbook(file_contents=raw_bytes)
            worksheet = workbook.sheet_by_index(0)
            
            rows = []
            for row_idx in range(worksheet.nrows):
                row = []
                for col_idx in range(worksheet.ncols):
                    cell = worksheet.cell(row_idx, col_idx)
                    if cell.ctype == xlrd.XL_CELL_NUMBER:
                        # Handle numbers
                        if cell.value == int(cell.value):
                            row.append(str(int(cell.value)))
                        else:
                            row.append(str(cell.value))
                    elif cell.ctype == xlrd.XL_CELL_DATE:
                        # Handle dates
                        row.append(str(cell.value))
                    else:
                        # Handle text and other types
                        row.append(str(cell.value))
                rows.append(row)
            
            return rows
        
        return []

    def _read_csv_file(self, raw_bytes):
        """Read CSV file and convert to list of rows"""
        # Clean bytes
        cleaned_bytes = raw_bytes.replace(b'\0', b'')
        
        # Try multiple encodings
        text_stream = None
        for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
            try:
                text_stream = io.TextIOWrapper(
                    io.BytesIO(cleaned_bytes), 
                    encoding=encoding,
                    errors='replace'
                )
                # Test read
                pos = text_stream.tell()
                test_line = text_stream.readline()
                text_stream.seek(pos)
                
                if test_line:
                    break
            except Exception:
                if text_stream:
                    text_stream.close()
                    text_stream = None
                continue
        
        if not text_stream:
            raise ValidationError(_("Could not decode CSV file with any encoding."))
        
        # Auto-detect delimiter
        text_stream.seek(0)
        sample = text_stream.read(1024)
        text_stream.seek(0)
        
        delimiter = ','
        for test_delimiter in [',', ';', '\t', '|']:
            if sample.count(test_delimiter) > sample.count(delimiter):
                delimiter = test_delimiter
        
        # Read CSV
        reader = csv.reader(text_stream, delimiter=delimiter, quotechar='"')
        rows = list(reader)
        text_stream.close()
        
        return rows

    def action_import(self):
        if not self.file_data:
            raise ValidationError(_("Please upload a file to import."))

        # Initialize counters
        processed_count = 0
        created_count = 0
        updated_count = 0
        skipped_count = 0
        error_count = 0

        try:
            # 1. Decode file from base64
            raw_bytes = base64.b64decode(self.file_data)
            _logger.info(f"File size: {len(raw_bytes)} bytes")

            # 2. Detect file type
            file_type = self._detect_file_type(raw_bytes)
            _logger.info(f"Detected file type: {file_type}")

            # 3. Read file based on type
            if file_type in ['xlsx', 'xls']:
                rows = self._read_excel_file(raw_bytes, file_type)
            else:
                rows = self._read_csv_file(raw_bytes)

            _logger.info(f"Total rows in file: {len(rows)}")

            # 4. Skip header rows (first 3 rows)
            if len(rows) < 4:
                raise ValidationError(_("File must have at least 2 rows (1 headers + 1 data row)."))

            data_rows = rows[1:]  # Skip first 3 header rows
            _logger.info(f"Data rows to process: {len(data_rows)}")

            # 5. Log sample of first few rows for debugging
            for i, row in enumerate(rows[:5]):
                _logger.info(f"Row {i}: {row[:19]}...")  # First 19 columns

            # 6. Initialize models
            Provinsi = self.env['vit.master_provinsi']
            KabKota = self.env['vit.master_kab_kota']
            dapodik = self.env['vit.master_dapodik']

            # 7. Process data rows
            for row_number, row in enumerate(data_rows, start=2):
                try:
                    # Validate row
                    if not row or len(row) < 19:
                        _logger.warning(f"Row {row_number}: Insufficient columns (got {len(row)}, need at least 19)")
                        skipped_count += 1
                        continue
                    
                    # Check required fields
                    npsn = str(row[4]).strip() if len(row) > 4 and row[0] else ''
                    name = str(row[5]).strip() if len(row) > 5 and row[2] else ''
                    provinsi_name = str(row[1]).strip() if len(row) > 1 and row[3] else ''
                    kab_kota_name = str(row[2]).strip() if len(row) > 2 and row[4] else ''
                    
                    # Skip if essential fields are empty
                    if not npsn or not name or not provinsi_name or not kab_kota_name:
                        _logger.warning(f"Row {row_number}: Missing required fields - NPSN: '{npsn}', Name: '{name}', Provinsi: '{provinsi_name}', Kab/Kota: '{kab_kota_name}'")
                        skipped_count += 1
                        continue

                    # --- Process Provinsi ---
                    try:
                        provinsi = Provinsi.search([('name', '=ilike', provinsi_name)], limit=1)
                        if not provinsi:
                            provinsi = Provinsi.create({'name': provinsi_name})
                            _logger.info(f"Created provinsi: {provinsi_name}")
                    except Exception as e:
                        _logger.error(f"Row {row_number}: Failed to process provinsi '{provinsi_name}': {e}")
                        error_count += 1
                        continue

                    # --- Process Kab/Kota ---
                    try:
                        kab_kota = KabKota.search([
                            ('name', '=ilike', kab_kota_name),
                            ('provinsi_id', '=', provinsi.id)
                        ], limit=1)
                        if not kab_kota:
                            kab_kota = KabKota.create({
                                'name': kab_kota_name,
                                'provinsi_id': provinsi.id
                            })
                            _logger.info(f"Created kab/kota: {kab_kota_name}")
                    except Exception as e:
                        _logger.error(f"Row {row_number}: Failed to process kab/kota '{kab_kota_name}': {e}")
                        error_count += 1
                        continue

                    # --- Process Mitra SPPG ---
                    try:
                        dapodik_vals = {
                        'name': name,
                        'npsn': npsn,
                        'status_kepemilikan': str(row[6]).strip(),
                        'bentuk_pendidikan': str(row[7]).strip(),
                        'status_sekolah': str(row[8]).strip(),
                        'alamat': str(row[9]).strip(),
                        'lintang': self._to_float(row[10]),
                        'bujur': self._to_float(row[11]),
                        'jumlah_pd': self._to_int(row[12]),
                        'jumlah_guru': self._to_int(row[13]),
                        'jumlah_tendik': self._to_int(row[14]),
                        'update_jumlah_pd': self._to_int(row[16]),
                        'update_jumlah_tendik': self._to_int(row[18]),
                        'provinsi_id': provinsi.id,
                        'kab_kota_id': kab_kota.id,
                                }

                        existing_mitra = dapodik.search([('npsn', '=', npsn)], limit=1)
                        if existing_mitra:
                            existing_mitra.write(dapodik_vals)
                            updated_count += 1
                            _logger.info(f"Updated dapodik: {npsn} - {name}")
                        else:
                            dapodik.create(dapodik_vals)
                            created_count += 1
                            _logger.info(f"Created dapodik: {npsn} - {name}")
                        
                        processed_count += 1
                        
                        # Periodic commit
                        if processed_count % 100 == 0:
                            self.env.cr.commit()
                            _logger.info(f"Processed {processed_count} records...")
                            
                    except Exception as e:
                        _logger.error(f"Row {row_number}: Failed to save dapodik '{npsn}': {e}")
                        error_count += 1
                        continue
                        
                except Exception as e:
                    _logger.error(f"Row {row_number}: Unexpected error: {e}")
                    error_count += 1
                    continue

            # Final commit
            self.env.cr.commit()

        except Exception as e:
            error_message = f"Import failed: {str(e)}"
            _logger.error(error_message)
            raise ValidationError(error_message)

        # Success message
        success_message = (
            f"Import completed successfully!\n"
            f"File type: {file_type.upper()}\n"
            f"Total data rows: {len(data_rows) if 'data_rows' in locals() else 0}\n"
            f"Processed: {processed_count} records\n"
            f"Created: {created_count} new records\n" 
            f"Updated: {updated_count} existing records\n"
            f"Skipped: {skipped_count} records\n"
            f"Errors: {error_count} records"
        )
        
        _logger.info(f"Import completed: {success_message}")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Import Completed'),
                'message': success_message,
                'type': 'success' if processed_count > 0 else 'warning',
                'sticky': True,
            }
        }