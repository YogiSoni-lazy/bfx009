sudo sed -i "s/RHT_COURSE=.*/RHT_COURSE=bfx009/" /etc/rht
sudo sed -i "s/RHT_VERSION_LOCK=.*/RHT_VERSION_LOCK='>=8.0,<9.0'/" /etc/rht
sudo systemctl restart dynolabs-update.service
pip install rht-labs-bfx009==8.0.3.dev13 --extra-index-url https://pypi.apps.tools-na.prod.nextcle.com/repository/labs/simple/
lab select bfx009
lab --version
source ~/.venv/labs/bin/activate
cd .venv/labs/lib/python3.6/site-packages/bfx009/
#git pull https://github.com/YogiSoni-lazy/bfx009.git
#git clone https://YogiSoni-lazy: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@github.com/YogiSoni-lazy/bfx009.git
