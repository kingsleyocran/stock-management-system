"use client";
import styles from "../page.module.css";
import { faDeleteLeft, faCheckCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState } from "react";
import { Loading } from "./utils";
import { ACCESS_KEY, REFRESH_KEY } from "../utils/constants";
import { makeOrder, totalQuantity, totalPrice } from "../utils";
export function OrderModal({ setShowOrderModal, setCartList, cartList }) {
  const [showSuccess, setShowSuccess] = useState(false);
  const [showLoading, setShowLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const handleCloseModel = (e) => {
    setShowOrderModal(false);
  };

  const handleDelete = (productId) => {
    setCartList((prevList) =>
      prevList.filter((product) => product.productId !== productId)
    );
  };

  const handleSubmit = async (e) => {
    setShowLoading(true);

    const sendData = cartList.map((item) => {
      const payload = {
        product_id: item.productId,
        quantity: parseInt(item.quantity),
      };
      return payload;
    });

    makeOrder(sendData).then((data) => {
      if (data?.error) {
        setErrorMsg(data.error);
      } else {
        setShowSuccess((prev) => !prev);
        setCartList([]);
      }
      setShowLoading(false);
    });
  };

  return (
    <>
      <div className={styles.modal}>
        <div className={`${styles.modalContent} ${styles.orderContainer}`}>
          <span className={styles.close} onClick={handleCloseModel}>
            &times;
          </span>

          {showLoading ? (
            <div className={`${styles.center} ${styles.done}`}>
              <Loading />
            </div>
          ) : (
            <>
              {showSuccess ? (
                <>
                  <div className={`${styles.center} ${styles.done}`}>
                    <>
                      <p>Thanks! your order will be delivered shortly</p>
                      <FontAwesomeIcon
                        icon={faCheckCircle}
                        className={styles.doneImage}
                      />
                    </>
                  </div>
                </>
              ) : (
                <>
                  {cartList.length > 0 ? (
                    <>
                      <p>{errorMsg}</p>
                      <h1 className={styles.orderTitle}> Your Order List</h1>
                      <ul>
                        {cartList.map((cart) => (
                          <div key={cart.productId} className={styles.listCart}>
                            <li>
                              {cart.quantity}{" "}
                              {cart.quantity === 1 ? "piece" : "pieces"} of{" "}
                              {cart.productName} for ${cart.totalAmount}
                            </li>
                            <span>
                              <FontAwesomeIcon
                                icon={faDeleteLeft}
                                onClick={() => handleDelete(cart.productId)}
                              />
                            </span>
                          </div>
                        ))}
                      </ul>

                      <div className={styles.orderContainerFooter}>
                        <div>
                          <button onClick={handleSubmit}>Order Now</button>
                        </div>
                        <div className={styles.orderContainerFooterDetails}>
                          <h1>
                            Total Pieces: {totalQuantity(cartList)} &nbsp; Total
                            Price: &nbsp; ${totalPrice(cartList)}
                          </h1>
                        </div>
                      </div>
                    </>
                  ) : (
                    <h1 className={styles.orderTitle}>
                      {" "}
                      You have no order list
                    </h1>
                  )}
                </>
              )}
            </>
          )}
        </div>
      </div>
    </>
  );
}
