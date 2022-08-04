FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    USER=compiler

# create $USER and home directory
RUN useradd --create-home --shell /bin/bash $USER && \
    chown -R $USER /home/$USER

# switch to non-root $USER
USER $USER

# update PATH for local pip installs
ENV PATH "$PATH:/home/$USER/.local/bin"

# update pip
RUN python -m pip install --upgrade pip

# enter src directory
WORKDIR /home/$USER/src

# copy and install packages
COPY . .
RUN pip install -r .devcontainer/requirements.txt
RUN pip install -r tests/requirements.txt