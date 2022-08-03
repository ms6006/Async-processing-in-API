import json
import requests
import os.path
from timeit import default_timer as timer

def output(sum):
    #Otwieramy plik do czytania
    File = open('output.json', 'r')
    
    #Jeśli plik nie jest pusty,
    #odczytujemy dane pliku i dodajemy nowe dane do pola
    #Jeśli plik jest pusty tworzymy nową data
    if os.path.getsize('output.json') > 0:
        json_data = ({
            "Primes": str(sum),
        }, )

        data = json.load(File)
        data["Sync"] += list(json_data)

    else:
        data = {
            "Time Async": "",
            "Time Sync": "",
            "Async": [],
            "Sync": [
                {
                    "Primes": str(sum),
                }
            ]
        }

    File.close()
    #Otwieramy plik do zapisu. Zapisujemy dane
    File = open('output.json', 'w')
    json.dump(data, File)
    File.close()

def create_output():
    #Jeżeli plik nie istnieje tworzymy go,
    #jeżeli plik istnieje to odczytujemy dane pliku
    #i resetujemy pole, w którym dane będziemy zapisywać
    if os.path.isfile('output.json') == 0:
        open('output.json', 'w')
    elif os.path.getsize('output.json') > 0:
        with open('output.json', 'r') as File:
            data = json.load(File)
            File.close()
        with open('output.json', 'w') as File:
            data["Sync"] = []
            json.dump(data, File)
            File.close()

results = []

def main():
    #Otwieramy plik i odczytujemy dane do request
    with open('values.json') as F:
        data = json.load(F)
        F.close()

    for i in data:
        #Wysyłamy requests i oczekujemy responses
        response = requests.get(f'http://localhost:8080/primes?start={i[0]}&end={i[1]}')
        print(response.text)
        #Zapisujemy wyniki do tabeli
        results.append(response.text)

if __name__ == '__main__':
    #Tworzymy plik output
    create_output()

    start = timer()
    main()
    end = timer()

    #Zapisujemy wyniki do pliku
    for r in results:
        output(r)

    #Zapisujemy czas wykonania do pliku  
    with open('output.json', 'r') as File:
        data = json.load(File)
        File.close()
    with open('output.json', 'w') as File:
        data["Time Sync"] = str(end - start)
        json.dump(data, File)
        File.close()

    print('Time: %f' % (end - start))
