import os
import panel as pn
import bokeh.server.contexts as ctx

def session_created(session_context: ctx.BokehSessionContext):
    # print(f"{session_context.id}")
    pass

def session_destroyed(session_context: ctx.BokehSessionContext):
    # print(f"Shutting app...")
    pass

pn.state.on_session_created(session_created)
pn.state.on_session_destroyed(session_destroyed)
