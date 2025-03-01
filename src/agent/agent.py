from langchain_core.tools import tool
from langchain_gigachat.chat_models import GigaChat
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent
import time

from src import args


def inicialization() -> CompiledGraph:
    memory = MemorySaver()
    args.model = GigaChat(
        credentials="YzJmZmJkNDUtYzE1Yy00ZTdhLWEyNjMtZDRjMDExZjFhMjI2OjQwZDM1YThmLTcwMWMtNGU1Yi05Zjc1LTM1MWQyM2MyZDM3NQ==",
        scope="GIGACHAT_API_PERS",
        model="GigaChat-Max",
        verify_ssl_certs=False,
        top_p=0.48
    )
    tools = [check_file_info]
    print('Агент стартанул')
    return create_react_agent(args.model,
                              checkpointer=memory,
                              tools=tools,
                            )


def check_file(text, agent, user_id) -> str:
    config = {"configurable": {"thread_id": user_id, "recursion_limit": "100"}}
    resp = agent.invoke({"messages": [("user", text)]}, config=config)
    print(resp)
    time.sleep(0.5)
    return resp["messages"][-1].content

#просто загружаем файл в гигчат

# def load_file_pages(text, user_id):
#     config = {"configurable": {"thread_id": user_id, "recursion_limit": "100"}}
#     agent.invoke{"messages": [("user", text)]}, config=config
#     print("\033[92m" + f"load_file_pages()" + "\033[0m")
#     time.sleep(0.5)

@tool
def check_file_info():
    """
    Ты - бот банка, который помогает клиентам находить ошибки в отчете по кредитной историей. Ты умеешь анализировать и воспринимать данные по кредитной истории в любом формате.
    В запросе от клиента обязательно будет приложен текст с его кредитной историей. Ты должен уметь анализировать текст с данными в любом формате.
    Текст, который клиент загрузил, — это все что есть у клиента, других данных не проси, а анализируй то, что загрузил клиент. Тебе важен только текст, что делать с этим текстом описано дальше.

    1) Найди различия в персональных данных от разных банков в файле и выведи какие различия ты нашел. ТОЛЬКО выведи разные значения фамилии, имени, отчества, даты рождения и паспорта. Клиент сам должен принять решение - это ошибка или нет. Главное покажи ему данные.
    - Если различия найдены и ты их показал, то посоветуй обратиться в сервис "Оспаривание ошибок в кредитной истории" в СберБанк Онлайн или в Бюро Кредитных историй (БКИ).
    - Если различий нет, то выведи, что обязательства принадлежат одному клиенту.

    2) Выведи индивидуальный рейтинг клиента и рекомендации к нему.

    3) Дай краткую аналитику по кредитной истории из файла в пяти пунктах.

    Формат ответа:
    - для всех клиентов выводи ответ четко по формату промта;
    - придерживайся дружелюбного и понятного стиля, используй простые слова, чтобы пояснить суть;
    - используй для анализа только данные из загруженного файла;
    Не выдумывай данные, не генерируй данные, которые противоречат данным из файла, анализируй только данные из файла.
    """
    # Подсвечивает вызов функции зеленым цветом
    print("\033[92m" + f"Bot requested check_file_info()" + "\033[0m")

