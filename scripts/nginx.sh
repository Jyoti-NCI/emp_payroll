
#!/usr/bin/bash

sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/default

sudo cp /home/ubuntu/emp_payroll/nginx/nginx.conf /etc/nginx/sites-available/emp_payroll
sudo ln -s /etc/nginx/sites-available/emp_payroll /etc/nginx/sites-enabled/
#sudo ln -s /etc/nginx/sites-available/recipes /etc/nginx/sites-enabled
#sudo nginx -t
sudo gpasswd -a www-data ubuntu
sudo systemctl restart nginx

