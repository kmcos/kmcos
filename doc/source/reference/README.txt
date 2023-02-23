Jan 19th 2023, updated the reference portion of the docs using robodoc. This required doing so on the Ubuntu side with an additional dependency installation.

I obtained robodoc from sourceforge through firefox on the Ubuntu linux virtual machine I was developing on.
https://sourceforge.net/projects/robodoc/

Then I did all of the below while logged into my kmcos python virtual environment (though the virtual envrionment was probably unnecessary for this installation).

I unzipped robodoc to my home directory (for convenience).
Then, I did something like this:
sudo ./configure; make; make install
This did not work, so I did something like the below.

sudo make uninstall
sudo make install

After doing so, typing "robodoc" and pressing enter showed an output that was promising, as though it was installed. I checked and it worked.

I think that the optimal install on Ubuntu would be something like this:
sudo ./configure
sudo make
sudo make install

After robodoc is installed, one can navigate to the kmcos/doc/source/reference/  and run "python3 generate_backend_reference.py" from the kmcos virtual environment.
