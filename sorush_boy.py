import asyncio
from splusthon import SoroushClient, events
from splusthon.sessions import StringSession

from openai import OpenAI

openai_client = OpenAI(api_key='sk-JcUnps6czsZz95dlsByQAXr9XPnJhWkoMMGKMXhPooij8wlg',base_url="https://apihub.agnes-ai.com/v1/")
import json
import os



BLACKLIST_FILE = "gif_blacklist.json"

def load_blacklist():
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return set()

def save_blacklist(blacklist):
    with open(BLACKLIST_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(blacklist), f, ensure_ascii=False, indent=2)
blocked_gif_ids = load_blacklist()
# NewMessage.Event(original_update=UpdateNewMessage(message=Message(id=149, peer_id=PeerUser(user_id=49245702), date=datetime.datetime(2026, 7, 17, 12, 59, 39, tzinfo=datetime.timezone.utc), message='.', out=False, mentioned=False, media_unread=False, silent=False, post=False, from_scheduled=False, legacy=False, edit_hide=False, pinned=False, noforwards=False, invert_media=False, from_id=PeerUser(user_id=49245702), fwd_from=None, via_bot_id=None, reply_to=None, media=None, reply_markup=None, entities=[], views=None, forwards=None, replies=None, edit_date=None, post_author=None, grouped_id=None, reactions=None, restriction_reason=[], ttl_period=None), pts=241, pts_count=1), pattern_match=None, message=Message(id=149, peer_id=PeerUser(user_id=49245702), date=datetime.datetime(2026, 7, 17, 12, 59, 39, tzinfo=datetime.timezone.utc), message='.', out=False, mentioned=False, media_unread=False, silent=False, post=False, from_scheduled=False, legacy=False, edit_hide=False, pinned=False, noforwards=False, invert_media=False, from_id=PeerUser(user_id=49245702), fwd_from=None, via_bot_id=None, reply_to=None, media=None, reply_markup=None, entities=[], views=None, forwards=None, replies=None, edit_date=None, post_author=None, grouped_id=None, reactions=None, restriction_reason=[], ttl_period=None))
# NewMessage.Event(original_update=UpdateNewChannelMessage(message=Message(id=98, peer_id=PeerChannel(channel_id=23094346), date=datetime.datetime(2026, 7, 17, 13, 4, 31, tzinfo=datetime.timezone.utc), message='.', out=False, mentioned=False, media_unread=False, silent=False, post=False, from_scheduled=False, legacy=False, edit_hide=False, pinned=False, noforwards=False, invert_media=False, from_id=PeerUser(user_id=49245702), fwd_from=None, via_bot_id=None, reply_to=None, media=None, reply_markup=None, entities=[], views=None, forwards=None, replies=None, edit_date=None, post_author=None, grouped_id=None, reactions=None, restriction_reason=[], ttl_period=None), pts=127, pts_count=1), pattern_match=None, message=Message(id=98, peer_id=PeerChannel(channel_id=23094346), date=datetime.datetime(2026, 7, 17, 13, 4, 31, tzinfo=datetime.timezone.utc), message='.', out=False, mentioned=False, media_unread=False, silent=False, post=False, from_scheduled=False, legacy=False, edit_hide=False, pinned=False, noforwards=False, invert_media=False, from_id=PeerUser(user_id=49245702), fwd_from=None, via_bot_id=None, reply_to=None, media=None, reply_markup=None, entities=[], views=None, forwards=None, replies=None, edit_date=None, post_author=None, grouped_id=None, reactions=None, restriction_reason=[], ttl_period=None))


blocked_words=['بچه کونی','بیو چک','بیوچک','رل پی','رلپی','فحش','لاشی','https://']
print()







SESSION_STRING = '1AwASaW0tc2VydmVyLnNwbHVzLmlyAbuFef4XemrFrCyEr4NnZ66Ydrtstd-F9me46RcqDkLZJ8v66Yyecwf9Fjhf2YvdjoatfL18Y9hFEkiwp1nBSTzrJVmt-86pBlIs5IpVYL4Ul2w2efbc7ZPBbnnKQQAgWogvz-fMWRO6khlTHtZfgADkG3Y6Lgdvg0_6f9pXKqhUXfr53smNMTIkniHCoaFnbzqzvQoNZWU6LEsHg_fey-K67sJUqsQhrdmqe7s144KCW8By00D0Tzs3KGZcOY6oP3fA6aS4vKSw9tT3r3UUmSa5N7qb3B240Bm53eWH2zHowqMmuSxJe-45TsxUvkbSDCAPADJiQKJOx9nGcDAzPiUg'

TARGET_ENTITY = -1000023094346
ADMINS_ID='AdnanEternal'
call_word="گاردی"
START_WORD='لیست قفل'


def is_private_chat(event):
    from splusthon.tl.types import PeerUser
    return isinstance(event.message.peer_id,PeerUser)






async def main():
    client = SoroushClient(StringSession(SESSION_STRING))
    
    await client.start()


 
    
    async def remove_warning_after_timeout(chat_id, message_id,timeout):
        await asyncio.sleep(timeout)
        await client.delete_messages(chat_id, message_ids=[message_id])
    




    @client.on(events.NewMessage)
    
    async def handler(event):
        # print(is_private_chat(event))
        
        asyncio.create_task(process_message(event))

        
    async def add_to_blacklist(event):
        replied_msg_id = event.reply_to_msg_id
        gif=await client.get_messages(entity=TARGET_ENTITY,ids=replied_msg_id)
        if gif.media.document.id not in blocked_gif_ids:
            blocked_gif_ids.add(gif.media.document.id)
            save_blacklist(blocked_gif_ids)
        await client.delete_messages(TARGET_ENTITY,ids=replied_msg_id)


    async def process_message(event):
        # if is_private_chat(event):
        #     if event.sender.username == ADMINS_ID:
        #         if event.sender.username:
        #             await client.send_message(event.sender.username,'')
                
                

        # if event.chat_id == TARGET_ENTITY:
                
            
            if any(word in event.raw_text.strip().lower() for word in blocked_words) :

                await client.delete_messages(event.chat_id, message_ids=[event.message.id])
                warn_msg = await client.send_message(TARGET_ENTITY, message='این کلمه ممنوعه!')
                asyncio.create_task(remove_warning_after_timeout(TARGET_ENTITY, warn_msg.id, 10))

            if event.raw_text == 'فیلتر محتوا':
                if event.reply_to == None:
                    return
                await add_to_blacklist(event)

            if event.message.media and event.message.document:
                gif_id = event.message.document.id
                if gif_id in blocked_gif_ids:
                    await client.delete_messages(event.chat_id, message_ids=[event.message.id])
            
            if event.raw_text.strip().lower()[:len(call_word)] == call_word:
                # await client.send_message(TARGET_ENTITY, message='6565')
                await event.reply(
                    openai_client.chat.completions.create(  
                        model="agnes-2.0-flash",
                        messages=[
                        {"role": "user", "content": event.raw_text.strip().lower()[len(call_word):]}
                    ]
                ).choices[0].message.content)

    await client.run_until_disconnected()

asyncio.run(main())



                
                # if call_word in event.raw_text.strip().lower():
               # print(last_msg.id,last_msg.text)
