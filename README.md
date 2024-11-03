# Plainews
## Distraction and clutter-free publication reading

[![PyPI version](https://badge.fury.io/py/plainews.svg)](https://badge.fury.io/py/plainews)

Check out our [Official website](https://nsobadzhiev.github.io/plainews-website/) :)

![Plainews screenshot](images/plainews_screenshot.jpg)

Reading news nowadays is broken. We are bombarded with ads to the point where the useful information we actually want to read is hidden away alongside a sea of upsells, ads and clickbait.

Plainews takes all that nonsense away and lets you focus on what you actually __want to__ read.

### Taking out the trash

We actually have the technology to eliminate the clutter, stop being bombarded with ads and just enjoy our content. Plainews downloads the webpage containing the publication you want to read and uses algorithms that strip away everything but the real, useful information. More on how that's done you will find further down the README.


### Summarizing bloated articles

Some articles are good, but too long. Often times authors beat around the bush or fill their text with information that's just not that interesting. Plainews can summarize articles so you feel up to date, without having to read long articles.

### Language-agnostic news - expat edition

Decouple language from locale. Sometimes you want to read news local to a region, but you also what to read it another language. Plainews can translate articles to any language you specify in the config.

### RSS

Yes, yet another RSS feed reader...
It's just the best way to get updates whenever your favorite blogs and newspapers have new content.

### TUI (Textual User interface)

Plainews rocks a beautiful (in my opinion) terminal interface. Not because I believe this is the future, but rather because I think it looks cool and it was a blast to develop :)

## Installing the application

Plainews is distributed via Pypi. You can find it [here](https://pypi.org/project/plainews/) online.
To install it, use PIP:

```commandline
pip install plainews
```
or
```commandline
python -m pip install plainews
```

Note that on some systems, you might have to use `python3` instead of `python`.
## Running the application

During the installation process, an executable will be placed alongside your python packages. This means you can start plainews by just writing:

```commandline
plainews
```

Keep in mind you need to have the location python installs packages in your `PATH`. In most Unix systems and MacOS, this should already be the case.
For Windows, you will get a warning in the terminal while you're installing plainews if the executable is not in `PATH` and there will be a link provided to an article how to add it (from System Settings -> Environment Variables).

## Configuration

Plainews depends on a configuration file for setting up your experience and the publications you want to read. 

This configuration is a yaml file. It should be located in one of the following locations:
* in the present working directory and named `config.yml`
* in the home directory and in the plainews folder - `~/.plainews/config.yml` 
* in the home directory and named `.plainews.yml`

### Format and available options

Here's the default yaml configuration:

```yaml
llm_model: ollama/llama3.1
llm_base_url: http://localhost:11434
language: english
feeds_file: feeds.pickle
articles_file: articles.pickle
followed_feeds:
    - https://rss.sueddeutsche.de/rss/Topthemen
    - https://feeds.arstechnica.com/arstechnica/index
history:
    keep_history: true
tts:
    cmd: say "<text>"
```

#### Followed feeds `followed_feeds`

The most important thing is the followed feeds. You need to add RSS feeds that you want to see in the app. Add the RSS URLs as you see them on the respective website.

Tip: You can also follow Medium users by adding the following URL: `https://medium.com/feed/@` followed by the user's name. For instance, my Medium RSS feed is `https://medium.com/feed/@n.sobadjiev_2847`

#### Feed and article files (`feeds_file` and `articles_file`)

This is just the location the saved feeds and articles will be stored on your computer. By default, a `.plainews` directory is created in your Home and these files are saved inside.

#### Keeping history (`history.keep_history`)

By default, RSS feeds don't return all articles ever published. Rather, they only return a finite number of items, typically the latest ones. Most RSS readers store older articles locally, so they can be still displayed. Plainews is no different, although we put less emphasis on that history. You can enable or disable it via the boolean `history.keep_history` property.
Additionally, the optional `max_history_items_per_feed` property specifies how many articles will be stored at a maximum. The default value is 150 and you can override it and specify something that you like better

### Text to speech (`tts`)

If you don't feel like reading, Plainews can also read articles out loud for you.
You can configure your own Text-to-Speech by providing a terminal command Plainews will execute on behalf of you with the contents of your article.
For instance, on MacOS, you can use the built-in `say` command yo leverage the system TTS. It doesn't provide the best voices or performance, but it's still a good place to start.
Populate the `cmd` property with the command to execute and use the `text` placeholder to specify where the article text should go.

### Smart features

Plainews has a few smart features provided by a large language model (that you provide). These features include:
* Summarizing articles
* Translating articles

Detailed information how these features and setup can be found in the [LLM_SETTINGS.md](LLM_SETTINGS.md) file.

### Dependencies

Poetry is used for dependency management. Before running, you need to make sure these dependencies are installed, either globally or in a (virtual) environment.

```commandline
poetry install
```

### Running the TUI

While being the root of the project, run:

```commandline
poetry run python app.py
```

## Information extractions

From my experience, most of the time the useful information can be extracted from a webpage easily using some locally running libraries. Namely, the [Newspaper3k](https://github.com/codelucas/newspaper/) python library does a fairly good job in this project.
In the future, we might use LLMs to handle the more complicated cases.
