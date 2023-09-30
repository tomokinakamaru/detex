from detex import detex


@detex
def section(args, cons):
    return f"\n1. {args}\n"


@detex
def item(args, cons):
    return f"\n- {cons}\n"
