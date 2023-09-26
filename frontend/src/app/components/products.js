"use client";
import Image from "next/image";
import styles from "../page.module.css";
import { Loading, CardLoader } from "../modal/utils";

export default function ProductList({
  searchProducts,
  handleClick,
  showProductsFound,
}) {
  return (
    <>
      {searchProducts.current?.length >= 1 ? (
        searchProducts.current?.map((product) => (
          <div
            className={styles.card}
            key={product.id}
            onClick={() => handleClick(product.id)}
          >
            <div className={styles.center}>
              <Image
                src={product.image ? product.image : "./store.svg"}
                alt={product.name}
                className={styles.storeLogo}
                width={200}
                height={200}
                priority
              />
            </div>
            <h2>
              {product.name} <span>-&gt; ${product.price}</span>
            </h2>
            <p>{product.description} </p>
            {/* <div className={styles.cardend}>
                  {product.status == "available"
                    ? `${product.quantity} in stock`
                    : "Out of Stock"}
                </div> */}
          </div>
        ))
      ) : (
        <>
          {showProductsFound ? (
            <CardLoader />
          ) : (
            // <div className={`${styles.center} ${styles.loading}`}>
            //   <Loading />
            // </div>
            <h1>
              We currently don&apos;t have {searchText.toLocaleLowerCase()}
              in store at the moment
            </h1>
          )}
        </>
      )}
    </>
  );
}
