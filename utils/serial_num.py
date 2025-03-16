def increment_counter(filepath="counter.txt"):
    """
    Reads a counter from a text file, increments it, and writes it back.

    Args:
        filepath (str): The path to the counter file. Defaults to "counter.txt".

    Returns:
        int: The incremented counter value, or None if an error occurred.
    """
    try:
        # Read the current counter value
        with open(filepath, "r") as f:
            counter = int(f.read().strip())

        # Increment the counter
        counter += 1

        # Write the updated counter value back to the file
        with open(filepath, "w") as f:
            f.write(str(counter))

        return counter

    except FileNotFoundError:
        # Handle the case where the file doesn't exist
        print(f"File '{filepath}' not found. Creating file and initializing counter to 1.")
        try:
            with open(filepath, "w") as f:
                f.write("1")
            return 1 #Return 1 because it's the first time
        except Exception as e:
            print(f"Error creating or initializing file: {e}")
            return None

    except ValueError:
        # Handle the case where the file content is not a valid integer
        print(f"Error: Invalid counter value in '{filepath}'. Resetting to 1.")
        try:
            with open(filepath, "w") as f:
                f.write("1")
            return 1
        except Exception as e:
            print(f"Error resetting counter: {e}")
            return None

    except Exception as e:
        # Handle other potential errors
        print(f"An error occurred: {e}")
        return None


# if __name__ == "__main__":
#     # Example usage:
#     counter_value = increment_counter()

#     if counter_value is not None:
#         print(f"Counter value: {counter_value}")

#     #Example of multiple calls:
#     for i in range(5):
#     new_count = increment_counter()
#     if new_count is not None:
#         print(f"Counter is now: {new_count}")