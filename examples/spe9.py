import jutuldarcy as jd
import matplotlib.pyplot as plt

pth = jd.test_file_path("SPE9", "SPE9.DATA")
res = jd.simulate_data_file(pth, convert = True)

fopr = res["FIELD"]["FOPR"]
days = res["DAYS"]
plt.plot(days, fopr)
plt.ylabel("Field oil production")
plt.xlabel("Days")
plt.show()
