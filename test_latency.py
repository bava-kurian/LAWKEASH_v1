import urllib.request
import json

url = 'http://localhost:8000/retrieve'
data = json.dumps({'query': 'What is section 302 of IPC?'}).encode('utf-8')
headers = {'Content-Type': 'application/json'}

try:
    print('Making first request (cold start)...')
    req1 = urllib.request.Request(url, data=data, headers=headers)
    res1 = urllib.request.urlopen(req1)
    res1_data = json.loads(res1.read())
    print(f'Cold Start Latency: {res1_data.get("latency_ms")} ms')

    print('Making second request (warm start, different query)...')
    data2 = json.dumps({'query': 'What is section 420 of IPC?'}).encode('utf-8')
    req2 = urllib.request.Request(url, data=data2, headers=headers)
    res2 = urllib.request.urlopen(req2)
    res2_data = json.loads(res2.read())
    print(f'Warm Start Latency: {res2_data.get("latency_ms")} ms')
except Exception as e:
    print(f'Error: {e}')
