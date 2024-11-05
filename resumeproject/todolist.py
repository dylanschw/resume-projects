# Create task array
tasks = []

# Function to create task
def addTask():
    task = input("Enter a task: ")
    tasks.append(task)
    print(f"'{task}' has been added to the list.")

# Function to list tasks
def listTasks():
    if not tasks:
        print("There are no tasks.")
    else:
        print("\nTasks:")
        for index, task in enumerate(tasks, start=1):
            print(f"Task {index}: {task}")

# Function to delete task
def deleteTask():
    listTasks()
    try:
        taskToDelete = int(input("Enter the number of the task to delete: ")) - 1
        if 0 <= taskToDelete < len(tasks):
            removed_task = tasks.pop(taskToDelete)
            print(f"'{removed_task}' has been deleted.")
        else:
            print(f"Task number {taskToDelete + 1} was not found.")
    except ValueError:
        print("Invalid input. Please enter a valid task number.")

if __name__ == "__main__":
    print("To-Do List")
    while True:
        print("\nSelect one of the following options:")
        print("------------------------------------")
        print("1. Add a new task")
        print("2. Remove a task")
        print("3. List all tasks")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            addTask()
        elif choice == "2":
            deleteTask()
        elif choice == "3":
            listTasks()
        elif choice == "4":
            print("Exiting the To-Do List application.")
            break
        else:
            print("Invalid option. Please select a valid choice.")
