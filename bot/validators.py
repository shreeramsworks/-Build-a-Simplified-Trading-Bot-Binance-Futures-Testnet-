import sys

def validate_inputs(args):
    """
    Validates CLI inputs and ensures required fields for specific order types are present.
    """
    errors = []
    
    # Check side
    if args.side.upper() not in ["BUY", "SELL"]:
        errors.append(f"Invalid side: {args.side}. Must be BUY or SELL.")

    # Check order type
    valid_types = ["MARKET", "LIMIT", "STOP"]
    if args.type.upper() not in valid_types:
        errors.append(f"Invalid type: {args.type}. Supported: {', '.join(valid_types)}.")

    # Validation logic for specific types
    order_type = args.type.upper()
    
    if order_type == "LIMIT":
        if args.price is None:
            errors.append("Error: --price is required for LIMIT orders.")
            
    if order_type == "STOP":
        if args.price is None or args.stop_price is None:
            errors.append("Error: Both --price and --stop-price are required for STOP (Stop-Limit) orders.")

    if args.quantity <= 0:
        errors.append(f"Invalid quantity: {args.quantity}. Must be greater than 0.")

    if errors:
        for error in errors:
            print(f"❌ {error}")
        sys.exit(1)

    return True
