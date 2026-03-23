

Okay to get this running:

```
git clone git@github.com:Anjaniputra15/IMC-prosperity.git
```

then to use the back tester.

```
(dont clone into this repo)
git clone https://github.com/GeyzsoN/prosperity_rust_backtester 
cd prosperity_rust_backtester
make install
```

Add this to your .zshrc or .bashrc

```
export PATH="$HOME/.cargo/bin:$PATH"
```

then

```
rust_backtester --trader <the bot/main.py> --dataset datasets/tutorial/prices_round_0_day_1.csv
```

You only need to link one prices as it will find the other one (trade/price)

```
https://prosperity.equirag.com/
```

Now should be able to load the log file into this website.




