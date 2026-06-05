import matplotlib.pyplot as plt

# ── LINE CHART ──────────────────────────────────────────
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales  = [150, 200, 170, 220, 300, 250]

plt.figure(figsize=(8, 4))          # canvas size (width, height) in inches
plt.plot(months, sales,
         color="steelblue",
         marker="o",                # dot at each data point
         linewidth=2,
         label="Monthly Sales")

plt.title("Monthly Sales - Line Chart")
plt.xlabel("Month")
plt.ylabel("Sales (units)")
plt.legend()                        # shows the label defined above
plt.tight_layout()
plt.show()

# ── BAR CHART ───────────────────────────────────────────
products  = ["Apples", "Bananas", "Cherries", "Dates"]
quantities = [45, 80, 30, 60]

plt.figure(figsize=(8, 4))
plt.bar(products, quantities,
        color=["#e74c3c", "#f39c12", "#8e44ad", "#27ae60"],
        width=0.5,                  # bar width (0–1)
        edgecolor="black")

plt.title("Product Quantity - Bar Chart")
plt.xlabel("Product")
plt.ylabel("Quantity")
plt.tight_layout()
plt.show()
