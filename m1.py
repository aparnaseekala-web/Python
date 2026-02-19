import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
np.random.seed(42)
routes = ['R1', 'R2', 'R3']
stops = ['Stop_A', 'Stop_B', 'Stop_C', 'Stop_D']
data = []
start_date = datetime.now() - timedelta(days=30)
for day in range(30):
    date = start_date + timedelta(days=day)
    for route in routes:
        for trip in range(10):
            hour = 7 + trip
            for i, stop in enumerate(stops):
                scheduled = date.replace(hour=hour, minute=i*10, second=0)
                
                if hour in [8, 9, 17]:
                    delay = np.random.normal(5, 2)
                else:
                    delay = np.random.normal(1, 1)
                actual = scheduled + timedelta(minutes=delay)
                data.append({
                    'route': route,
                    'stop': stop,
                    'scheduled': scheduled,
                    'actual': actual
                })
df = pd.DataFrame(data)
df['delay'] = (df['actual'] - df['scheduled']).dt.total_seconds() / 60
df['hour'] = df['actual'].dt.hour
print("\n" + "="*50)
print("BUS DELAY ANALYSIS")
print("="*50)
print(f"\nTotal Trips: {len(df):,}")
print(f"Average Delay: {df['delay'].mean():.2f} minutes")
print(f"Max Delay: {df['delay'].max():.2f} minutes")
on_time = (df['delay'].abs() <= 2).sum() / len(df) * 100
print(f"On-Time %: {on_time:.1f}%")
print("\nWorst Routes:")
for route, delay in df.groupby('route')['delay'].mean().sort_values(ascending=False).items():
    print(f"  {route}: {delay:.2f} min")
print("\nWorst Stops:")
for stop, delay in df.groupby('stop')['delay'].mean().sort_values(ascending=False).items():
    print(f"  {stop}: {delay:.2f} min")
print("\nWorst Hours:")
for hour, delay in df.groupby('hour')['delay'].mean().sort_values(ascending=False).head(3).items():
    print(f"  {hour}:00 - {delay:.2f} min")
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0, 0].hist(df['delay'], bins=30, color='blue', edgecolor='black')
axes[0, 0].set_title('Delay Distribution')
axes[0, 0].set_xlabel('Delay (minutes)')
hourly = df.groupby('hour')['delay'].mean()
axes[0, 1].bar(hourly.index, hourly.values, color='green')
axes[0, 1].set_title('Average Delay by Hour')
axes[0, 1].set_xlabel('Hour')
route_delay = df.groupby('route')['delay'].mean()
axes[1, 0].barh(route_delay.index, route_delay.values, color='orange')
axes[1, 0].set_title('Average Delay by Route')
stop_delay = df.groupby('stop')['delay'].mean()
axes[1, 1].bar(stop_delay.index, stop_delay.values, color='red')
axes[1, 1].set_title('Average Delay by Stop')
plt.tight_layout()
plt.savefig('bus_analysis.png', dpi=150)
df.to_csv('bus_data.csv', index=False)
print("\n" + "="*50)
print("DONE!")
print("="*50 + "\n")     
plt.show()