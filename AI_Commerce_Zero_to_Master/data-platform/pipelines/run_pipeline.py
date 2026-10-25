from bronze_ingest import run as bronze
from silver_transform import run as silver
from gold_warehouse import run as gold
from future_features import run as features

if __name__ == "__main__":
    print("1 Bronze:", bronze())
    print("2 Silver:", silver())
    print("3 Gold/Warehouse:", gold())
    print("4 Future ML features:", features())
