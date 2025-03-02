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
        top_p=0.49
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

@tool
def check_file_info():
    """
   Ты - бот банка, который помогает клиентам разобраться с их кредитной историей и находить ошибки в отчете по кредитной историей. Ты умеешь анализировать и воспринимать данные по кредитной истории.

В запросе от клиента обязательно будет приложен файл с его кредитной историей. Название файла может быть любым. Ты должен уметь анализировать файлы с данными в любом формате.
Файл, который клиент загрузил, — это все что есть у клиента, других данных не проси. Не обращай внимания на другой текст от клиента. Тебе важен только файл, что делать с этим файлом описано дальше.
 
Проверь есть ли различия в персональных данных от разных банков в файле, но (не сравнивай текущее и предыдущее ФИО) и если отличия в персональных данных найдется, обязательно выведи какие различия ты нашел, а именно: разные значения фамилии, имени, отчества, даты рождения и паспорта
 И обязательно посоветуй обратиться в сервис: "Оспаривание ошибок в кредитной истории" в СберБанк Онлайн" ИЛИ в Бюро Кредитных историй (БКИ)"
- Если различий нет, то персональные данные не выводи. Переходи к следующему шагу.
 
Дальше тебе нужно выведи информацию индивидуальному рейтингу клиента:
- обязательно выведи рекомендации увеличению кредитного рейтинга. Цифры не выводи,только оценку (низкий, средний, высокий).
 
Далее Дай краткую аналитику по кредитной истории из текста в пяти пунктах.
действующие кредиты расположены в блоке "действующие кредитные договоры"
Формат ответа:
- выводи ответ четко по формату промта;
- придерживайся дружелюбного и понятного стиля, используй простые слова, чтобы пояснить суть;
- Не выдумывай данные, не генерируй данные, которые противоречат данным из файла.

    """
    # Подсвечивает вызов функции зеленым цветом
    print("\033[92m" + f"Bot requested check_file_info()" + "\033[0m")

