# The ADACS Workshop Template

This repository is The ADACS template for creating websites for workshops.

1. **Please _do not fork this repository directly on GitHub._** Instead, please use GitHub's
   "template" function following [the instructions below](#creating-a-repository) to copy this
   `workshop-template` repository and customize it for your workshop.

2. Please *do your work in your repository's `gh-pages` branch*, since that is what is
   [automatically published as a website by GitHub][github-project-pages].

If you run into problems,
or have ideas about how to make this process simpler,
please [get in touch](#getting-and-giving-help).
The pages on [customizing your website][customization],
the [FAQ][faq],
and the [design notes][design] have more detail on what we do and why.
And please note:
if you are teaching Git,
please [create a separate repository](#setting-up-a-separate-repository-for-learners)
for your learners to practice in.

## Creating a Repository

1.  Log in to GitHub.
    (If you do not have an account, you can quickly create one for free.)
    You must be logged in for the remaining steps to work.

2.  On this page (<https://github.com/ADACS-Australia/ADACS_Carpentries_Template>),
    click on the green "Use this template" button (top right)
    Alternatively, use this link: [Use this template](https://github.com/new?template_name=ADACS_Carpentries_Template&template_owner=ADACS-Australia).

3.  Select the owner for your new repository. This should be ADACS, unless you are using this for your own lessons (not recommended - use the <https://github.com/carpentries/workshop-template> site instead).

4.  Choose a name for your workshop website repository.
    This name should have the form `YYYY-MM-DD-topic`,
    e.g., `2025-01-15-AstroCoding`,
    where `YYYY-MM-DD` is the start date of the workshop.

5.  Make sure the repository is public, leave "Include all branches" unchecked, and click
on "Create repository from template".
You will be redirected to your new copy of the workshop template respository.

6. Your new website will be rendered at `https://adacs-australia.github.io/YYYY-MM-DD-topic`.

## Customizing Your Website (Required Steps)

There are two ways of customizing your website. You can either:

- edit the files directly in GitHub using your web browser
- clone the repository on your computer and update the files locally (recommended)

### Updating the files on GitHub in your web browser

1.  Go into your newly-created repository,
    which will be at `https://github.com/adacs-australia/YYYY-MM-DD-topic`.

3.  Ensure you are on the gh-pages branch by clicking on the branch under the drop
    down in the menu bar (see the note below):

    ![screenshot of this repository's GitHub page showing the "Branch" dropdown menu expanded with the "gh-pages" branch selected](fig/select-gh-pages-branch.png?raw=true)

3.  Edit the header of `index.md` to customize the list of instructors,
    workshop venue, etc.
    You can do this in the browser by clicking on it in the file view on GitHub
    and then selecting the pencil icon in the menu bar:

    ![screenshot of top menu bar for GitHub's file interface with the edit icon highlighted in the top right](fig/edit-index-file-menu-bar.png?raw=true)

    Editing hints are embedded in `index.md`,
    and full instructions are in [the customization instructions][customization].

4.  Edit `_config.yml` to customize certain site-wide variables, such as: 
    `title` (overall title for all pages), `pre_survey` and `post_survey` links, 
    and maybe the workshop order section. 
    There should be no need to change the `carpentries` or `curriculum` values.
    Editing hints are embedded in `_config.yml`,
    and full instructions are in [the customization instructions][customization].

5. Edit the `schedule.html` file to edit the schedule for your upcoming workshop. This file is
   located in the `_includes/dc/` directory.

### Working locally

> Note: you don't have to do this, if you have already updated your site using the web interface.


If you are already familiar with Git, you can clone the repository to your desktop, edit `index.md`,
`_config.yml`, and `schedule.html` following the instruction above there, and push your changes back to the repository.

```shell
git clone https://github.com/adacs-australia/YYYY-MM-DD-topic
```

In order to view your changes once you are done editing, if you have docker installed (see the
[installation instructions below](#installing-software)), you can preview your site locally with:

```shell
make docker-serve
```
and go to <http://0.0.0.0:4000> to preview your site.

Before pushing your changes to your repository, we recommend that you also check for any potential
issues with your site by running:

```shell
make workshop-check
```

Once you are satisfied with the edits to your site, commit and push the changes to your repository.
A few minutes later, you can go to the GitHub Pages URL for your workshop site and preview it. [The finished
page should look something like this](fig/completed-page.png?raw=true).


## Optional but Recommended Steps


### Update your repository description and link your website

At the top of your repository on GitHub you'll see

~~~
No description, website, or topics provided. — Edit
~~~

Click 'Edit' and add:

1.  A very brief description of your workshop in the "Description" box (e.g., "Oomza University workshop, Dec. 2016")

2.  The URL for your workshop in the "Website" box (e.g., `https://gvwilson.github.io/2016-12-01-oomza`)

This will help people find your website if they come to your repository's home page.

### Update the content of the README file

You can change the `README.md` file in your website's repository, which contains these instructions,
so that it contains a short description of your workshop and a link to the workshop website.


## Additional Notes

**Note:**
please do all of your work in your repository's `gh-pages` branch,
since [GitHub automatically publishes that as a website][github-project-pages].

**Note:**
this template includes some files and directories that most workshops do not need,
but which provide a standard place to put extra content if desired.
See the [design notes][design] for more information about these.

Further instructions are available in [the customization instructions][customization].
This [FAQ][faq] includes a few extra tips (additions are always welcome)
and these notes on [the background and design][design] of this template may help as well.


## Editing Existing Lessons
The lesson `setup` is included by default and may need a few edits including:

- Updating the acknowledgement for an in-person event.
- Update the note about who requested the training and link to the relevant ADACS page.
- Update assumed knowledge and any software tools that are required to participate in the workshop.
- Update the ice-breaker question

Other lessons can be included by making a .md file in the `_episodes` directory following the format of the `setup.md` lesson.

Ordering of lessons is by default alphabetic, so you can prefix your lessons with `01` etc to dictate the order.
This makes it annoying to reorder lessons, so instead you can change the lesson order in the `episode_order` section of the `_config.yml` file (at the end).

## Update schedule
Edit `_includes/dc/schedule.html` file to reflect the correct day/time/order of lessons.

## Creating Extra Pages

In rare cases,
you may want to add extra pages to your workshop website.
You can do this by putting either Markdown or HTML pages in the website's root directory
and styling them according to the instructions give in
[the lesson template][lesson-example].


## Installing Software

If you want to set up Jekyll so that you can preview changes on your own machine before pushing them
to GitHub, you must install the software described in the lesson example [setup
instructions](https://carpentries.github.io/lesson-example/setup.html#jekyll-setup-for-lesson-development).

## Setting Up a Separate Repository for Learners

If you are teaching Git,
you should create a separate repository for learners to use in that lesson.
You should not have them use the workshop website repository because:

* your workshop website repository contains many files that most learners don't need to see during
  the lesson, and

* you probably don't want to accidentally merge a damaging pull request from a novice Git user into
  your workshop's website while you are using it to teach.

You can call this repository whatever you like, and add whatever content you need to it.

## Getting and Giving Help

We are committed to offering a pleasant setup experience for our learners and organizers.
If you find bugs in our instructions,
or would like to suggest improvements,
please [file an issue][issues]
or [mail us][email].

[email]: mailto:team@carpentries.org
[customization]: https://carpentries.github.io/workshop-template/customization/index.html
[dc-site]: https://datacarpentry.org
[design]: https://carpentries.github.io/workshop-template/design/index.html
[faq]: https://carpentries.github.io/workshop-template/faq/index.html
[github-project-pages]: https://help.github.com/en/github/working-with-github-pages/creating-a-github-pages-site
[issues]: https://github.com/carpentries/workshop-template/issues
[lesson-example]: https://carpentries.github.io/lesson-example/
[self-organized-workshop-form]: https://amy.carpentries.org/forms/self-organised/
[swc-site]: https://software-carpentry.org
[lc-site]: https://librarycarpentry.org
