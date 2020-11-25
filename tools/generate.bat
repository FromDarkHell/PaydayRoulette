@ECHO OFF

call scraper.exe

git add --all
git commit --author="Payday Roulette Updater <>" -m "Add new gear / heists due to patch" -a
git push