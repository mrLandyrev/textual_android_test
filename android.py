from textual.app import App, ComposeResult
from textual.widgets import Button, LoadingIndicator, Input, Label
from textual.containers import Container
from textual.widget import Widget
from textual.message import Message
from textual.reactive import reactive
from textual import on
import asyncio

class QuestionMessage(Message):
    query: str

    def __init__(self, query: str) -> None:
        self.query = query
        super().__init__()

class Question(Widget):
    query = ""

    def compose(self) -> ComposeResult:
        yield Input(value="secret word")
        yield Button()

    @on(Button.Pressed)
    def send_pressed(self, event: Button.Pressed) -> None:
        self.post_message(QuestionMessage(self.query))

    @on(Input.Changed)
    def query_changed(self, event: Input.Changed) -> None:
        self.query = event.value


class TestApp(App):
    loading = reactive(False, recompose=True)
    response = reactive("", recompose=True)

    def compose(self) -> ComposeResult:
        with Container():
            if self.loading:
                yield LoadingIndicator()
            else:
                yield Label(self.response)
                yield Question()

    @on(QuestionMessage)
    def question(self, message: QuestionMessage) -> None:
        self.loading = True
        self.run_worker(self.process_query(message.query))
    
    async def process_query(self, query: str) -> None:
        def test():
            response = query_engine.query(query)
            self.response = response.response
        await asyncio.to_thread(test)
        self.loading = False
    
        


app = TestApp()
app.run()