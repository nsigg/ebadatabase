def printBegin(title, year):
    print(f'Starting to import {title} of year {year}')


def printSummary(time, lines):
    print(f'It took {time} seconds to import {lines} lines', end='\n\n')


def printProcessingStatus(lines):
    print(f'Scanning {lines} lines', end='\r')


def printMissingLEICodes(missingLEICodes: list, year: int, missingLines: int = 0):
    if missingLines > 0:
        print(f'Missing LEI Codes resulted in {missingLines} missing lines.')
    print(f'{len(missingLEICodes)} missing LEI codes for year {year}:')
    for leiCode in missingLEICodes:
        print(leiCode)

def printCompleteSummary(time):
    # Gibst am Ende eine Zusammenfassung aus
    print(f'Finished creating database! It took {time} seconds.')
