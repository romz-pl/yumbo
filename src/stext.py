from PIL import Image
import io
import streamlit as st

def show_fig(fig):
    fig.tight_layout()

    # Save the figure to a buffer and display
    with io.BytesIO() as buf:
        fig.savefig(buf, format="WebP", pil_kwargs={"lossless":True, "quality":70, "method":3} )
        # fig.savefig(buf, format="png", pil_kwargs={"compress_level": 9})
        # st.write(buf.getbuffer().nbytes)
        st.image(buf)

