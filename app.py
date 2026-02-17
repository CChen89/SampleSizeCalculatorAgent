import chainlit as cl
from illiad import askasource
import time

@cl.on_chat_start
async def on_chat_start():
    print("A new chat session has started!")

    # Create User Session with chat history attached 
    cl.user_session.set("chat_history", [])
    #time.sleep(2)
    #await cl.Message(content="Hello! I am your go/SPAT assistant designed by AbbVie DSS OASiS team. What can I do for you today?").send()

@cl.on_message
async def main(message: cl.Message):

    # Get chat history 
    chat_history = cl.user_session.get("chat_history")

    # Get response from Illiad
    response = askasource(message.content, history=chat_history)

    # Send a response back to the user
    if response["success"] == True:
        formatted_m = f"{response["data"]['content']} \n \n References: {response["data"]["references"][0]["id"]} - {response["data"]["references"][0]["filename"]}"
        await cl.Message(
            content=formatted_m,
        ).send()
        
        # Save the chat history
        chat_history.append({"role": "user", "content": message.content})
        chat_history.append({"role": "system", "content": response["data"]['content']})
        cl.user_session.set("chat_history", chat_history)

    if response["success"] == False:
        await cl.Message(
            content=f"No success",
        ).send()