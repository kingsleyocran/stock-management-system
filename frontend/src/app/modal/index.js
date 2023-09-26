"use client";
import Image from "next/image";
import styles from "../page.module.css";
import { useState, useCallback, useRef } from "react";

export function ProductModel({
  product,
  setShowModal,
  setCartList,
  isLoggedIn,
}) {
  const displayProduct = { ...product }[0];
  const quantity = useRef(1);
  const [totalAmount, setTotalAmount] = useState(displayProduct.price);
  const handleChange = useCallback(
    (e) => {
      quantity.current = e.target.value;
      setTotalAmount(displayProduct.price * quantity.current);
    },
    [setTotalAmount, displayProduct.price, quantity]
  );

  const handleCloseModel = (e) => {
    setShowModal(false);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (quantity.current <= 0) {
      alert("Can't order 0 quantity");
    } else {
      const orderDetails = {
        productId: displayProduct.id,
        productName: displayProduct.name,
        quantity: quantity.current,
        totalAmount: totalAmount,
      };
      setCartList((prev) => [...prev, orderDetails]);
      setShowModal(false);
    }
  };

  return (
    <>
      <div className={styles.modal}>
        <div className={styles.modalContent}>
          <span className={styles.close} onClick={handleCloseModel}>
            &times;
          </span>

          <div className={styles.modalDivision}>
            <div>
              <Image
                src={
                  displayProduct.image ? displayProduct.image : "./store.svg"
                }
                alt={displayProduct.category}
                className={`${styles.storeLogo} ${styles.modalImage}`}
                width={220}
                height={200}
              />
            </div>

            <div className={styles.modalDescription}>
              <div>
                <h1>{displayProduct.name} </h1>
              </div>
              <div>
                <p>{displayProduct.description}</p>
              </div>
              <div>
                <p>Price: ${displayProduct.price}</p>
              </div>
              {isLoggedIn ? (
                <>
                  <div>
                    <p>Quantity</p>
                  </div>

                  <div>
                    <input
                      type="number"
                      min={1}
                      max={displayProduct.quantity}
                      value={quantity.current}
                      onChange={handleChange}
                    />
                  </div>

                  <div>
                    <p>Total Amount &nbsp; -&gt; ${totalAmount} </p>
                  </div>

                  <div>
                    <button type="submit" onClick={handleSubmit}>
                      Add to Cart
                    </button>
                  </div>
                </>
              ) : (
                ""
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
