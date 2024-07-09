# Algorithmic Trading

Need: OPEN ACCOUNT - ANGEL BROKING

Generate API From SMARTAPI: https://smartapi.angelbroking.com/signin

# Steps for Installation 
1. Install Anaconda Python

2. Install API modules for Angel API

3. Copy the script to respective folder

4. Edit the required parameters 

5. Run the script

# Trading Logic
Main Trading Loop:

The script runs continuously, checking the time and executing trades at 9:22 AM for BankNIFTY and 12:30 PM for NIFTY on specified trading days.

For BankNIFTY at 9:22 AM:

Fetches the latest price and calculates the strike price.

Places sell orders for both Call and Put options.

Sets stop-loss orders for both options.

For NIFTY at 12:30 PM:

Similar logic to BankNIFTY but applied to NIFTY options.

# Order and Stop-Loss Functions:

Functions order and sl are defined to place regular and stop-loss orders using the Angel Broking API.
modify_order is defined to modify existing orders.

# End of Day Handling
Exit Positions:
The script checks the time until 3:10 PM and attempts to modify existing orders to exit all positions at the end of the trading day.

# Conclusion
Final Output:
Prints "day trading done" after all trading actions are completed for the day.
