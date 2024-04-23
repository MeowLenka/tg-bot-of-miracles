import asyncio
import aiohttp
from deep_translator import GoogleTranslator

# async def get_file(i, url, session):
#     response = await session.get(url, allow_redirects=True)
#     await write_file(response)
#     response.close()
#
#
# async def write_file(response):
#     filename = response.url.name
#     data = await response.read()
#     with open(f'./city_images/{filename}', 'wb') as file:
#         file.write(data)
#
#
# async def main():
#     url = 'https://loremflickr.com/640/480/russia'
#     tasks = []
#     session = aiohttp.ClientSession()
#     for i in range(30):
#         task = asyncio.create_task(get_file(i, url, session))
#         tasks.append(task)
#     await asyncio.gather(*tasks)
#     await session.close()


if __name__ == '__main__':
    langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
    text = 'happy coding'
    translator = GoogleTranslator(source='auto', target='ru')
    translated = translator.translate(text=text)
    print(translated)
