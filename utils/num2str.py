def number_to_words_rupees(amount):
    """
    Converts an integer amount in rupees to its equivalent in words.

    Args:
        amount: An integer representing the amount in rupees.

    Returns:
        A string representing the amount in words.
    """

    if not isinstance(amount, int):
        return "Invalid input. Please provide an integer amount."

    if amount < 0:
        return "Amount cannot be negative."

    if amount == 0:
        return "Zero Rupees"

    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]

    def convert_hundreds(num):
        if num == 0:
            return ""
        elif num < 10:
            return ones[num]
        elif num < 20:
            return teens[num - 10]
        else:
            return tens[num // 10] + (" " + ones[num % 10]) if num % 10 else tens[num // 10]

    def convert_thousands(num):
        if num == 0:
            return ""
        elif num < 100:
            return convert_hundreds(num)
        else:
            return ones[num // 100] + " Hundred" + (" " + convert_hundreds(num % 100) if num % 100 else "")

    def convert_lakhs(num):
        if num == 0:
            return ""
        elif num < 100:
            return convert_hundreds(num)
        else:
            return ones[num//100] + " Hundred" + (" " + convert_hundreds(num % 100) if num % 100 else "")

    def convert_crores(num):
        if num == 0:
            return ""
        elif num < 100:
            return convert_hundreds(num)
        else:
            return ones[num//100] + " Hundred" + (" " + convert_hundreds(num % 100) if num % 100 else "")

    result = ""

    crores = amount // 10000000
    amount %= 10000000

    lakhs = amount // 100000
    amount %= 100000

    thousands = amount // 1000
    amount %= 1000

    hundreds = amount

    if crores:
        result += convert_hundreds(crores) + " Crore" + (" " if (lakhs or thousands or hundreds) else "")
    if lakhs:
        result += convert_hundreds(lakhs) + " Lakh" + (" " if (thousands or hundreds) else "")
    if thousands:
        result += convert_thousands(thousands) + " Thousand" + (" " if hundreds else "")
    if hundreds:
        result += convert_hundreds(hundreds)

    return result.strip() + " Rupees"