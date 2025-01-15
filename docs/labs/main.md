# Executing code labs

During this event, we will guide you through a series of labs using Google Cloud Shell.

Cloud Shell is a fully interactive, browser-based environment for learning, experimenting, and managing Google Cloud projects. It comes preloaded with the Google Cloud CLI, essential utilities, and a built-in code editor with Cloud Code integration, enabling you to develop, debug, and deploy cloud apps entirely in the cloud.

Below you can find a screenshot of Cloud Shell.

![](../img/cloud_shell_window.png)

It is based on Visual Studio Code and hence looks like a normal IDE. However, on the right hand side you see the tutorial you will be working through. When you encouter code chunks in the tutorial, there are two icons on the right hand side. One to copy the code chunk to your clipboard and the other one to insert it directly into the terminal of Cloud Shell.

## Things to know before you get started

There are a few common pitfall that may arise while you work on the labs. Please read them before you start.

<div class="mdbook-alerts mdbook-alerts-tip">
<p class="mdbook-alerts-title">
  <span class="mdbook-alerts-icon"></span>
  Tip
</p>
<p>
If you accidentally close the Cloud Shell window, just
<a href="https://shell.cloud.google.com/cloudshell/open?page=editor&show=ide" target="_blank">open it again</a>.
Do not press the <b>START LABS</b> button below again.
</p>
</div>

<div class="mdbook-alerts mdbook-alerts-tip">
<p class="mdbook-alerts-title">
  <span class="mdbook-alerts-icon"></span>
  Tip
</p>
<p>
In case there is no open project in Cloud Shell, please open <code>cloudshell_open/bootkon</code>.
</p>
</div>

<div class="mdbook-alerts mdbook-alerts-tip">
<p class="mdbook-alerts-title">
  <span class="mdbook-alerts-icon"></span>
  Tip
</p>
<p>
All code chunks in the tutorial are expected to be executed from the <code>cloudshell_open/bootkon</code> directory.</p>
</div>

<div class="mdbook-alerts mdbook-alerts-tip">
<p class="mdbook-alerts-title">
  <span class="mdbook-alerts-icon"></span>
  Tip
</p>
<p>In case you no longer see the tutorial on the right-hand side, open it again with:</p>
<pre><code class="language-bash">cd ~/cloudshell_open/bootkon
cloudshell launch-tutorial .TUTORIAL.md
</code></pre>
</div>

---

To start the code labs, press the button below. The source repository will be cloned automatically, and the tutorial will appear on the right-hand side for easy reference. Continue your journey inside Cloud Shell.

[![Start labs](https://img.shields.io/badge/start_labs-blue?style=for-the-badge)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/{{ GITHUB_REPOSITORY }}&page=editor&tutorial=.TUTORIAL.md&show=ide&cloudshell_workspace=)
