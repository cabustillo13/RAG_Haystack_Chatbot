from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import PromptTemplate,AnswerParser,BM25Retriever,PromptNode
from haystack.pipelines import Pipeline
from haystack import Document
import kaggle
import pandas as pd
import os
from dotenv import load_dotenv
import chainlit as cl

# Loading up OpenAI Api Key from environment variables
load_dotenv("../.env")
load_dotenv()
MY_API_KEY = os.getenv("OPENAI_API_KEY")

# Initializing document store, use_bm25 when we can't use GPU
document_store = InMemoryDocumentStore(use_bm25=True)

# Downloading lyrics database from Kaggle
kaggle_dataset_id = "deepshah16/song-lyrics-dataset"
kaggle.api.authenticate()
kaggle.api.dataset_download_files(kaggle_dataset_id, path='../', unzip=True)

# We chose two artists for starters
df_bts = pd.read_csv("../csv/BTS.csv")
df_lady_gaga = pd.read_csv("../csv/LadyGaga.csv")

df_lyrics = pd.concat([df_bts, df_lady_gaga], axis=0)

# Renaming first column to id and generating the correct numbers
col_names = df_lyrics.columns.to_list()
col_names[0] = "id"
df_lyrics.columns = col_names
df_lyrics.reset_index(drop=True, inplace=True)
df_lyrics["id"] = df_lyrics.index + 1


# Document store expects a content column
df_lyrics = df_lyrics.rename(columns={"Lyric": "content"})

# Converting dataframe to list of dictionaires
document_store.write_documents(df_lyrics.to_dict('records'))


rag_prompt = PromptTemplate(
    prompt="""Synthesize a brief answer from the following text for the given question.
            Provide a clear and concise response related to music lyrics and the artists provided.
            Your answer should be in your own words and be no longer than 50 words.
            \n\n Music Lyrics: {join(documents)} \n\n Question: {query} \n\n Answer:""",
    output_parser=AnswerParser(),
)

retriever = BM25Retriever(document_store=document_store, top_k=2)
pn = PromptNode("gpt-3.5-turbo", 
                api_key=MY_API_KEY, 
                model_kwargs={"stream":False},
                default_prompt_template=rag_prompt)


# Setting up the pipeline
pipe = Pipeline()
pipe.add_node(component=retriever, name="retriever", inputs=["Query"])
pipe.add_node(component=pn, name="prompt_node", inputs=["retriever"])

@cl.on_message
async def main(message: str):
    # Use the pipeline to get a response
    output = pipe.run(query=message)

    # Create a Chainlit message with the response
    response = output['answers'][0].answer
    msg = cl.Message(content=response)

    # Send the message to the user
    await msg.send()