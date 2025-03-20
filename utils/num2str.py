def number_to_words_rupees(amount):
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
            return tens[num // 10] + (" " + ones[num % 10] if num % 10 else "")

    def convert_below_thousand(num):
        if num == 0:
            return ""
        elif num < 100:
            return convert_hundreds(num)
        else:
            return ones[num // 100] + " Hundred" + (" " + convert_hundreds(num % 100) if num % 100 else "")

    result = ""

    crores = amount // 10000000
    amount %= 10000000

    lakhs = amount // 100000
    amount %= 100000

    thousands = amount // 1000
    amount %= 1000

    hundreds = amount

    if crores:
        result += convert_below_thousand(crores) + " Crore" + (" " if (lakhs or thousands or hundreds) else "")
    if lakhs:
        result += convert_below_thousand(lakhs) + " Lakh" + (" " if (thousands or hundreds) else "")
    if thousands:
        result += convert_below_thousand(thousands) + " Thousand" + (" " if hundreds else "")
    if hundreds:
        result += convert_below_thousand(hundreds)  

    return result.strip() + " Rupees"

# Example:
print(number_to_words_rupees(5600))  
print(number_to_words_rupees(5678))  
