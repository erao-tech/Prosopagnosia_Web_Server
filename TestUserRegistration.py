#!/usr/bin/python3.7

#  Copyright 2020 EraO Prosopagnosia Helper Dev Team, Liren Pan, Yixiao Hong, Hongzheng Xu, Stephen Huang, Tiancong Wang
#
#  Supervised by Prof. Steve Mann (http://www.eecg.toronto.edu/~mann/)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import argparse
import asyncio

from aiohttp import ClientSession, MultipartWriter, ClientConnectionError, ClientPayloadError, ClientResponseError, \
    FormData


async def upload_file(url, username, password, responses):
    mpw = MultipartWriter()

    fd = FormData()
    fd.add_field('username', username)
    fd.add_field('password', password)

    async with ClientSession() as session:
        try:
            async with session.post(url, data=fd) as response:
                response = await response.read()
                response_str = response.decode('utf-8')
                responses[response_str] = responses.get(response_str, 0) + 1
        except ClientConnectionError:
            responses['CONNECTION_ERR'] = responses.get('CONNECTION_ERR', 0) + 1
        except ClientPayloadError:
            responses['PAYLOAD_ERR'] = responses.get('PAYLOAD_ERR', 0) + 1
        except ClientResponseError:
            responses['RESPONSE_ERR'] = responses.get('RESPONSE_ERR', 0) + 1


async def status_printer(requests, responses):
    while True:
        print("Uploaded: %d files, responses: %s" % (requests['i'], responses))
        await asyncio.sleep(1.0)


async def load_gen(url, username, password, rate, n_uploads):
    responses = {}
    requests = {'i': 0}
    asyncio.create_task(status_printer(requests, responses))
    while n_uploads == 0 or requests['i'] < n_uploads:
        upload_task = upload_file(url, username, password, responses)
        asyncio.create_task(upload_task)
        requests['i'] += 1
        await asyncio.sleep(1.0 / rate)


async def load_gen():
    responses = {}
    requests = {'i': 0}
    asyncio.create_task(status_printer(requests, responses))

    upload_task = upload_file("http://localhost:5000/api/register", "admin", "admin", responses)
    asyncio.create_task(upload_task)
    requests['i'] += 1
    await asyncio.sleep(1.0 / 20)

    upload_task = upload_file("http://localhost:5000/api/register", "test1", "", responses)
    asyncio.create_task(upload_task)
    requests['i'] += 1
    await asyncio.sleep(1.0 / 20)

    upload_task = upload_file("http://localhost:5000/api/register", "", "123", responses)
    asyncio.create_task(upload_task)
    requests['i'] += 1
    await asyncio.sleep(1.0 / 20)

    upload_task = upload_file("http://localhost:5000/api/register", "test3   ", "123", responses)
    asyncio.create_task(upload_task)
    requests['i'] += 1
    await asyncio.sleep(1.0 / 20)

    upload_task = upload_file("http://localhost:5000/api/register", "    ", "123", responses)
    asyncio.create_task(upload_task)
    requests['i'] += 1
    await asyncio.sleep(1.0 / 20)

    for var in range(10):
        upload_task = upload_file("http://localhost:5000/api/register", "handsomeFredkk" + str(var), "fakedPWD",
                                  responses)
        asyncio.create_task(upload_task)
        requests['i'] += 1
        await asyncio.sleep(1.0 / 20)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate file uploading load',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(load_gen())
