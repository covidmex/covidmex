import sys
import urllib2
import csv
import json
from datetime import datetime, timedelta, date

if len(sys.argv) == 3 and sys.argv[1] and sys.argv[2]:
    try:
        start_date=datetime.strptime(sys.argv[1], '%Y-%m-%d')
        end_date=datetime.strptime(sys.argv[2], '%Y-%m-%d')
    except:
        raise NameError('Error: Invalid format for start date and/or end date. Format should be YYYY-MM-DD')

    if start_date <= end_date:
        for n in range(int ((end_date - start_date).days)+1):
            single_date = start_date + timedelta(n)

            single_date_day = single_date.day
            single_date_month = single_date.month
            single_date_year = single_date.year

            reports = [{
                        'type': 'sospechosos',
                        'id': 's',
                        'url': 'https://serendipia.digital/wp-content/uploads/%s/%02d/Tabla_casos_sospechosos_COVID-19_%s.%02d.%02d-Table-1.csv' % (single_date_year, single_date_month, single_date_year, single_date_month, single_date_day),
                        'header': ('caso','estado','sexo','edad','sintomas','rt-pcr','procedencia','llegada')},
                       {'type': 'confirmados',
                        'id': 'c',
                        'url': 'https://serendipia.digital/wp-content/uploads/%s/%02d/Tabla_casos_positivos_COVID-19_resultado_InDRE_%s.%02d.%02d-Table-1.csv' % (single_date_year, single_date_month, single_date_year, single_date_month, single_date_day),
                        'header':('caso','estado','sexo','edad','sintomas','rt-pcr','procedencia','llegada')}]

            for report in reports:
                sys.stdout.write('Downloading CSV from: %s \n' % report['url'])

                try:
                    response = urllib2.urlopen(report['url'])
                except urllib2.URLError as e:
                    sys.stdout.write(str(e.reason))
                    sys.stdout.write('\n\n')
                    continue

                csv_content = response.read()
                response.close()

                # Remove the first line of the csv
                csv_content = csv_content.split('\n',2)[2]

                # Remove the last 2 lines of the content
                #csv_content = csv_content[:csv_content[:csv_content.rfind('\n')].rfind('\n')]

                # Save temp file
                file = open('/tmp/covid-temp.txt', 'w')
                file.write(csv_content)
                file.close()

                filename = 'json/%s-%02d-%02d-%s.json' % (single_date_year, single_date_month, single_date_day, report['id'])
                json_file = open(filename, 'w')

                json_file.write('{"datos":[')
                sys.stdout.write('Processing')
                first_line = True

                with open('/tmp/covid-temp.txt', 'r') as csv_file:
                    reader = csv.DictReader(csv_file, report['header'])
                    for row in reader:
                        if unicode(row['caso'], 'utf-8').isnumeric():
                            if first_line is not True:
                                json_file.write(',\n')

                            # Clean Strings
                            row['estado'] = row['estado'].replace('*', '')
                            row['estado'] = row['estado'].replace('\n', '')
                            row['procedencia'] = row['procedencia'].replace('*', '')
                            row['procedencia'] = row['procedencia'].replace('\n', '')

                            sys.stdout.write('.')
                            json.dump(row, json_file, ensure_ascii=False, indent=3)
                            first_line = False
                        else:
                            sys.stdout.write(' [DONE]\n\n')

                csv_file.close()
                json_file.write(']}')
                json_file.close()
    else:
        print 'Error: start date should be less or equal than end date'
else:
    print 'Error: start date and end date required.'
