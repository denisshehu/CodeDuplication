FROM python:3.6-slim

RUN apt-get update && apt-get install -y curl

RUN curl -sL https://deb.nodesource.com/setup_13.x | bash - && apt-get install -y git nodejs cloc

WORKDIR /usr/jquery-data

COPY prep.py .

COPY jquery_releases.csv .

RUN python prep.py

# Docker caches results, so if you want to add custom steps to this dockerfile
# (maybe you want to copy in more files) then consider adding these steps below here.
# Otherwise you will need to download all versions of jQuery everytime you add new 
# steps.

# Install the packages required to generate the heatmap
RUN pip install -U pandas matplotlib

# Add the manually constructed code snippets to the directory /usr/manual-clones.
WORKDIR /usr/manual-clones

ADD code_snippets .

WORKDIR /usr

COPY jsinspect jsinspect

RUN npm install -g ./jsinspect

# Increase the amount of memory nodejs can allocate, this
# prevents JsInspect from running into the GC issues. 
ENV NODE_OPTIONS=--max-old-space-size=4000

WORKDIR /usr/jquery-data

# Open a bash prompt, such that you can execute commands 
# such as `cloc`. 
ENTRYPOINT ["bash"]

# Add the source code to Docker
WORKDIR /usr/src

ADD src .

# Run the tool
RUN python main.py