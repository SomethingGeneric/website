# git

I set up basic git repo hosting via SSH by following this guide: [https://romanzolotarev.com/git.html](https://romanzolotarev.com/git.html)

To make a repo:

```
ssh git@xhec.dev git init --bare test-repo.git
mkdir test-repo
cd test-repo
micro README.md
git init
git add README.md
git commit -m "readme"
git remote add origin git@xhec.dev:test-repo.git
git push origin master
```

I later made a script so that you can simply

```
ssh git@xhec.dev mkrepo <some_repo_name>
```

~~The page [https://xhec.dev/git.html](https://xhec.dev/git.html) is made with a shell script thru crontab~~
