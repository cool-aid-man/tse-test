from __future__ import annotations

from typing import Optional, Tuple

from ..adapter import StringAdapter
from ..interface import verb_required_block
from ..interpreter import Context


__all__: Tuple[str, ...] = ("AssignmentBlock",)


class AssignmentBlock(verb_required_block(False, parameter=True)):  # type: ignore
    """
    Variables are useful for choosing a value and referencing it later in a tag.
    Variables can be referenced using brackets as any other block.

    **Usage:** ``{=(<name>):<value>}``

    **Aliases:** ``assign, let, var``

    **Payload:** value

    **Parameter:** name

    **Examples:** ::

        {=(prefix):!}
        The prefix here is `{prefix}`.
        # The prefix here is `!`.

        {assign(day):Monday}
        {if({day}==Wednesday):It's Wednesday my dudes!|The day is {day}.}
        # The day is Monday.

    .. rubric:: How Argument Parsing Works

    Once a variable is assigned, its value can be parsed (split and indexed)
    to extract specific parts.

    **Simple — Basic Token Access**

    ``{variable(n)}`` splits the stored value by **spaces** and returns the
    ``n``-th token. Indexing is **1-based**:

    ::

        {=(msg):Hello world foo bar}
        {msg(1)}  -> Hello
        {msg(2)}  -> world

    ``0`` is special and returns the **last** element:

    ::

        {msg(0)}  -> bar

    **Advanced — Negative Indexing, Ranges & Custom Delimiters**

    Negative indices count **backwards** from the end (``-1`` = second-to-last):

    ::

        {msg(-1)}  -> foo
        {msg(-2)}  -> world

    Appending ``+`` to an index gives a **range** — everything from that
    position to the end:

    ::

        {msg(-2+)}  -> world foo bar

    A **custom delimiter** can be passed as the payload to change how
    the value is split. The syntax is ``{variable(index):delimiter}``:

    ::

        {=(data):apple.banana.cherry}
        {data(2):.}  -> banana

    Variables can be **nested** to perform multi-level parsing:

    ::

        {=(raw):A-B,C,D}
        {=(part):{raw(2):-}}
        # part = "B,C,D"
        {part(1):,}  -> B
        {part(2):,}  -> C

    """

    ACCEPTED_NAMES: Tuple[str, ...] = ("=", "assign", "let", "var")

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.parameter is None:
            return None
        ctx.response.variables[ctx.verb.parameter] = StringAdapter(str(ctx.verb.payload))
        return ""
