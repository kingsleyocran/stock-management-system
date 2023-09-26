"use client";
import Image from "next/image";
import styles from "../page.module.css";
import Link from "next/link";
import {
  faCartShopping,
  faUserCircle,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { ProductModel } from "../modal";
import { OrderModal } from "../modal/order";
import { AddProductModel } from "../modal/product";
import { useState } from "react";
import { UserProfile } from "../modal/profile";
import { logOut, removeToken } from "../utils";

export default function Header({
  singleProduct,
  cartList,
  setCartList,
  userDetails,
}) {
  const [showUserProfile, setShowUserProfile] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [showOrderModal, setShowOrderModal] = useState(false);
  const [showAddProductModal, setShowAddProductModal] = useState(false);

  const handleOrderClick = (e) => {
    setShowOrderModal((prev) => !prev);
  };

  const handleLogOut = (e) => {
    logOut().then(() => {
      removeToken();
      window.location.reload();
    });
  };

  const handleAddProductClick = (e) => {
    setShowAddProductModal((prev) => !prev);
  };

  const handleProfileModal = (e) => {
    setShowUserProfile((prev) => !prev);
  };

  return (
    <>
      <header className={styles.header}>
        <div className={styles.headerLeft}>
          <Link href="/">
            <Image
              src="/store.svg"
              alt="Store logo"
              className={styles.storeLogo}
              width={100}
              height={60}
              priority
            />
          </Link>
          <h1>My Store</h1>
        </div>

        {showOrderModal ? (
          <OrderModal
            setShowOrderModal={setShowOrderModal}
            setCartList={setCartList}
            cartList={cartList}
          />
        ) : (
          ""
        )}

        {showModal ? (
          <ProductModel
            product={singleProduct.current}
            setShowModal={setShowModal}
            setCartList={setCartList}
            isLoggedIn={Object.keys(userDetails).length !== 0}
          />
        ) : (
          ""
        )}

        {showAddProductModal ? (
          <AddProductModel onShow={handleAddProductClick} />
        ) : (
          ""
        )}

        {showUserProfile ? (
          <UserProfile onShow={handleProfileModal} userDetails={userDetails} />
        ) : (
          ""
        )}
        <div className={styles.headerRight}>
          {Object.keys(userDetails).length !== 0 ? (
            <>
              <div className={styles.headerRightItem}>
                {userDetails?.first_name ? (
                  <span className={styles.welcome}>
                    WELCOME {userDetails?.first_name.toUpperCase()}
                  </span>
                ) : (
                  ""
                )}
              </div>

              <div className={styles.headerRightItem}>
                {cartList?.length > 0 ? (
                  <>
                    <span className={styles.badge}>{cartList.length}</span>
                  </>
                ) : (
                  ""
                )}
                <FontAwesomeIcon
                  icon={faCartShopping}
                  onClick={handleOrderClick}
                />
              </div>

              <div className={`${styles.headerRightItem} ${styles.profilePic}`}>
                {userDetails?.profile_pic.length < 1 ? (
                  <>
                    <FontAwesomeIcon
                      icon={faUserCircle}
                      className={`${styles.storeLogo} ${styles.profilePic}`}
                    />
                  </>
                ) : (
                  <>
                    <Image
                      src={userDetails.profile_pic}
                      alt="Store logo"
                      className={`${styles.storeLogo} ${styles.profilePic}`}
                      width={100}
                      height={60}
                      priority
                    />
                  </>
                )}
                <div className={styles.profileDetails}>
                  <a onClick={handleProfileModal}>Change Profile</a>
                  {userDetails?.is_admin ? (
                    <a onClick={handleAddProductClick}>Add Product</a>
                  ) : (
                    ""
                  )}
                  {userDetails?.is_admin || userDetails?.is_sales_rep ? (
                    <Link href="/reports">Reports</Link>
                  ) : (
                    ""
                  )}
                  <a onClick={handleLogOut}>Logout</a>
                </div>
              </div>
            </>
          ) : (
            <>
              <div className={styles.headerRightItem}>
                <Link href="/auth/signin"> Sign In </Link>
              </div>
              <div className={styles.headerRightItem}>
                <Link href="/auth/signup"> Sign Up </Link>
              </div>
            </>
          )}
        </div>
      </header>
    </>
  );
}
