from pyrogram import Client
from pyrogram.errors import FloodWait, PeerIdInvalid, UserDeactivated, UserDeactivatedBan
import asyncio
import config
from ..logging import LOGGER

assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        # Initialize only valid session strings to avoid None errors
        self.clients = {}
        
        if config.STRING1:
            self.one = Client(
                name="RAUSHANAss1",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(config.STRING1),
                no_updates=True,
                max_concurrent_transmissions=1,  # Limit concurrent transmissions
                sleep_threshold=10,               # Sleep on flood wait
                workdir="./session1/"            # Separate work directories
            )
            self.clients[1] = self.one
            
        if config.STRING2:
            self.two = Client(
                name="RAUSHANAss2",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(config.STRING2),
                no_updates=True,
                max_concurrent_transmissions=1,
                sleep_threshold=10,
                workdir="./session2/"
            )
            self.clients[2] = self.two
            
        if config.STRING3:
            self.three = Client(
                name="RAUSHANAss3",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(config.STRING3),
                no_updates=True,
                max_concurrent_transmissions=1,
                sleep_threshold=10,
                workdir="./session3/"
            )
            self.clients[3] = self.three
            
        if config.STRING4:
            self.four = Client(
                name="RAUSHANAss4",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(config.STRING4),
                no_updates=True,
                max_concurrent_transmissions=1,
                sleep_threshold=10,
                workdir="./session4/"
            )
            self.clients[4] = self.four
            
        if config.STRING5:
            self.five = Client(
                name="RAUSHANAss5",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                    no_updates=True,
                max_concurrent_transmissions=1,
                sleep_threshold=10,
                workdir="./session5/"
            )
            self.clients[5] = self.five

    async def start_single_client(self, client_num, client):
        """Start a single client with proper error handling"""
        try:
            await client.start()
            
            # Join support channels with retry logic
            for channel in ["Silenthrex"]:
                try:
                    await client.join_chat(channel)
                    await asyncio.sleep(2)  # Small delay between joins
                except Exception as e:
                    LOGGER(__name__).warning(f"Failed to join {channel}: {e}")
                    continue
            
            assistants.append(client_num)
            
            # Send startup message with error handling
            try:
                await client.send_message(config.LOGGER_ID, f"Assistant {client_num} Started")
            except Exception as e:
                LOGGER(__name__).error(f"Assistant {client_num} failed to access log group: {e}")
                return False
                
            # Store client info
            if hasattr(client, 'me') and client.me:
                client.id = client.me.id
                client.name = client.me.mention
                client.username = client.me.username
                assistantids.append(client.id)
                LOGGER(__name__).info(f"Assistant {client_num} Started as {client.name}")
                return True
            else:
                LOGGER(__name__).error(f"Failed to get user info for Assistant {client_num}")
                return False
                
        except FloodWait as e:
            LOGGER(__name__).warning(f"FloodWait for Assistant {client_num}: {e.value}s")
            await asyncio.sleep(float(e.value))  # Cast to float
            return await self.start_single_client(client_num, client)
        except (UserDeactivated, UserDeactivatedBan) as e:
            LOGGER(__name__).error(f"Assistant {client_num} is deactivated/banned: {e}")
            return False
        except Exception as e:
            LOGGER(__name__).error(f"Failed to start Assistant {client_num}: {e}")
            return False

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistants...")
        
        # Start clients with delays to avoid rate limiting
        started_clients = []
        
        for client_num, client in self.clients.items():
            try:
                success = await self.start_single_client(client_num, client)
                if success:
                    started_clients.append(client_num)
                # Add delay between starting clients
                await asyncio.sleep(3)
            except Exception as e:
                LOGGER(__name__).error(f"Error starting client {client_num}: {e}")
                continue
        
        if started_clients:
            LOGGER(__name__).info(f"Successfully started {len(started_clients)} assistants: {started_clients}")
        else:
            LOGGER(__name__).warning("No assistants were started successfully")

    async def stop(self):
        LOGGER(__name__).info(f"Stopping Assistants...")
        stop_tasks = []
        
        for client_num, client in self.clients.items():
            if client and hasattr(client, 'is_connected') and client.is_connected:
                try:
                    stop_tasks.append(client.stop())
                except Exception as e:
                    LOGGER(__name__).warning(f"Error stopping client {client_num}: {e}")
        
        if stop_tasks:
            await asyncio.gather(*stop_tasks, return_exceptions=True)
