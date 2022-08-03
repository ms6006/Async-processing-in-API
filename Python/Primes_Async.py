import asyncio
import aiohttp
import json
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
            "Primes": str(sum)
        }, )

        data = json.load(File)
        data["Async"] += list(json_data)

    else:
        data = {
            "Time Async": "",
            "Time Sync": "",
            "Async": [
                {
                    "Primes": str(sum),
                }
            ],
            "Sync": []
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
            data["Async"] = []
            json.dump(data, File)
            File.close()

def get_tasks(session):
    tasks = []
    #Otwieramy plik i odczytujemy dane do request
    with open('values.json') as F:
        data = json.load(F)
        F.close()

    #Tworzymy taski i zapisujemy do tabeli
    for i in data:
        tasks.append(asyncio.create_task(session.get(f'http://localhost:8080/primes?start={i[0]}&end={i[1]}')))

    return tasks

results = []

async def main():

    async with aiohttp.ClientSession() as session:
        #Otrzymujemy taski
        tasks = get_tasks(session)
        #Wysyłamy requests i oczekujemy responses
        responses = await asyncio.gather(*tasks)
        #Zapisujemy wyniki do tabeli
        for response in responses:
            results.append(await response.text())

if __name__ == '__main__':
    try:
        #Tworzymy plik output
        create_output()

        start = timer()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        end = timer()
        
        #Dla wszystkich wyników
        for r in results:
            #Zapisujemy wyniki do pliku
            output(r)
            print(r)
            
        #Zapisujemy czas wykonania do pliku    
        with open('output.json', 'r') as File:
            data = json.load(File)
            File.close()
        with open('output.json', 'w') as File:
            data["Time Async"] = str(end - start)
            json.dump(data, File)
            File.close()

        print('Time: %f' % (end - start))

    except Exception as e:
        print(str(e))

    finally:
        loop.close()
