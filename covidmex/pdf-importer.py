# -*- coding: utf-8 -*-
""" Covidmex PDF Importer

This script parses the URL given as parameter, then downloads the PDF report
(suspects and confirmed cases for a certain date), performs a conversion of
the document tables based on a fixed layout with camelot and then finally
generates and validates a JSON file for covidmex import process.

Usage:
    $ python pdf-importer.py <URL>

Example:
        $ python pdf-importer.py \
        https://www.gob.mx/cms/uploads/attachment/file/546159/Tabla_casos_positivos_COVID-19_resultado_InDRE_2020.04.10.pdf

Requirements:
    Python 3.5+
    The following modules:
        camelot-py==0.7.3
        lxml==4.5.0
        tldextract==2.2.2
        wget==3.2

Todo:
    * Improve camelot.read_pdf() processing time.
    * Upload the generator JSON file automatically.

"""

import os
import sys
import shutil
import wget
import json
import camelot
import time
from re import search
from datetime import datetime, timedelta, date
from tldextract import extract

RED   = "\033[1;31m"
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

def main():
    pdf_temp = '/tmp/covid.tmp.pdf'
    header = ('caso','estado','sexo','edad','sintomas','rt-pcr','procedencia','llegada')

    if len(sys.argv) == 2:
        url = sys.argv[1]
        tld = extract(url)

        if tld.suffix not in ['gob.mx']:
            sys.stdout.write('Error: %sInvalid URL. URL should be from gob.mx domain%s.\n' % (RED, RESET))
            sys.exit(1)

        try:
            result = search("([0-9]{4}\.[0-9]{2}\.[0-9]{2})", url)
            report_date=datetime.strptime(result[0], '%Y.%m.%d')
        except:
            sys.stdout.write('Error: %sInvalid format for report date URL. Format should contain date YYYY.MM.DD%s .\n' % (RED, RESET))
            sys.exit(1)

        if 'sospechosos' in url:
            report_type = 's'
        elif 'positivos' in url:
            report_type = 'c'

        json_filename = 'json/%s-%02d-%02d-%s.json' % (report_date.year, report_date.month, report_date.day, report_type)

        sys.stdout.write('Downloading PDF from: %s \n' % url)

        try:
            file = wget.download(url, pdf_temp)
        except:
            sys.stdout.write('%sError%s\n' % (RED, RESET))
            sys.exit(1)

        # Overwrite file if already exists
        if os.path.exists(pdf_temp):
            shutil.move(file,pdf_temp)

        sys.stdout.write(' [%sDONE%s]\nPerforming PDF conversion (this may take a while): ' % (GREEN, RESET))
        start = time.time()

        try:
            tables = camelot.read_pdf(pdf_temp, parallel=True, pages='all')
        except:
            sys.stdout.write('%sInvalid format. Downloaded file should be a PDF%s.\n' % (RED, RESET))
            sys.exit(1)

        end = time.time()
        hours, rem = divmod(end-start, 3600)
        minutes, seconds = divmod(rem, 60)
        sys.stdout.write(' %02dh %02dm %02.2fs [%sDONE%s]\n' % (int(hours),int(minutes),seconds, GREEN, RESET))

        json_file = open(json_filename, 'w')
        json_file.write('{"datos":[')
        first_line = True
        first_row = True
        counter = 1
        sys.stdout.write('Creating JSON file: ')

        for table in tables:
            for row in table.data:
                if first_line is False:
                    if first_row is False:
                        json_file.write(',\n')

                    data = dict(zip(header, row))

                    # Clean Strings
                    data['estado'] = data['estado'].replace('*', '')
                    data['estado'] = data['estado'].replace('\n', '')
                    sys.stdout.write('%s.%s' % (BOLD, RESET))
                    json.dump(data, json_file, ensure_ascii=False, indent=3)
                    first_row = False

                first_line = False
                counter += 1

        json_file.write(']}')
        sys.stdout.write(' [%sDONE%s]\n' % (GREEN, RESET))
        json_file.close()

        # JSON validation
        sys.stdout.write('Validating JSON: ')
        json_file = open(json_filename, 'r')
        json_data = json_file.read()

        try:
            json.loads(json_data)
            sys.stdout.write('%sfile is valid%s.\n' % (GREEN, RESET))
            sys.stdout.write('\n')
            sys.stdout.write('File %s%s%s created successfully.\n' % (BOLD, json_filename, RESET))
            sys.stdout.write('%s%02d%s cases processed from %s%d%s pages.\n' % (BOLD, counter, RESET, BOLD, len(tables), RESET))
        except ValueError as error:
            sys.stdout.write('\033[1;31mJSON is invalid, check for errors\033[0;0m.\n')

        json_file.close()
        sys.stdout.write('\n')
        sys.exit(0)
    else:
        sys.stdout.write('%sError: report URL is required%s.\n' % (RED, RESET))
        sys.stdout.write('Usage: %spython pdf-importer.py <URL>%s.\n' % (CYAN, RESET))
        sys.exit(1)

if __name__ == "__main__":
    main()
