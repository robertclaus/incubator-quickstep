/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 **/

#include "utility/ScopedReassignment.hpp"

#include <cstddef>
#include <string>
#include <vector>

#include "utility/Macros.hpp"

#include "gtest/gtest.h"

namespace quickstep {

/**
 * @brief A test class that is movable but not copyable.
 */
class NonCopyable {
 public:
  explicit NonCopyable(const int value)
      : value_(value) {}

  explicit NonCopyable(NonCopyable &&other)
      : value_(other.value_) {}

  NonCopyable& operator=(NonCopyable &&other) {
    value_ = other.value_;
    return *this;
  }

  int value() const {
    return value_;
  }

 private:
  int value_;

  DISALLOW_COPY_AND_ASSIGN(NonCopyable);
};

/**
 * @brief A test class that is copyable but not movable.
 */
class NonMovable {
 public:
  explicit NonMovable(const int value)
      : value_(value) {}

  explicit NonMovable(const NonMovable &other)
      : value_(other.value_) {}

  NonMovable& operator=(const NonMovable &other) {
    value_ = other.value_;
    return *this;
  }

  int value() const {
    return value_;
  }

 private:
  int value_;
};

/**
 * @brief A test class that is copyable and movable.
 */
class CopyableMovable {
 public:
  explicit CopyableMovable(const int value)
      : value_(value) {}

  explicit CopyableMovable(const CopyableMovable &other)
      : value_(other.value_),
        copy_constructed_(true) {}

  explicit CopyableMovable(CopyableMovable &&other)
      : value_(other.value_) {}

  CopyableMovable& operator=(const CopyableMovable &other) {
    value_ = other.value_;
    copy_assigned_ = true;
    return *this;
  }

  CopyableMovable& operator=(CopyableMovable &&other) {
    value_ = other.value_;
    copy_assigned_ = false;
    return *this;
  }

  int value() const {
    return value_;
  }

  bool copy_constructed() const {
    return copy_constructed_;
  }

  bool copy_assigned() const {
    return copy_assigned_;
  }

 private:
  int value_;
  bool copy_constructed_ = false;
  bool copy_assigned_ = false;
};

TEST(ScopedReassignment, NonCopyableTest) {
  NonCopyable var_a(10);
  NonCopyable other(20);
  {
    ScopedReassignment<NonCopyable> reassign(var_a, std::move(other));
    EXPECT_EQ(20, var_a.value());
  }
  EXPECT_EQ(10, var_a.value());

  NonCopyable var_b(30);
  {
    ScopedReassignment<NonCopyable> reassign(var_b, NonCopyable(40));
    EXPECT_EQ(40, var_b.value());
  }
  EXPECT_EQ(30, var_b.value());
}

TEST(ScopedReassignment, NonMovableTest) {
  NonMovable var_a(10);
  NonMovable other(20);
  {
    ScopedReassignment<NonMovable> reassign(var_a, other);
    EXPECT_EQ(20, var_a.value());
  }
  EXPECT_EQ(10, var_a.value());

  NonMovable var_b(30);
  {
    ScopedReassignment<NonMovable> reassign(var_b, NonMovable(40));
    EXPECT_EQ(40, var_b.value());
  }
  EXPECT_EQ(30, var_b.value());
}

TEST(ScopedReassignment, CopyableMovableTest) {
  CopyableMovable var_a(10);
  CopyableMovable other(20);
  {
    ScopedReassignment<CopyableMovable> reassign(var_a, other);
    EXPECT_EQ(20, var_a.value());
    EXPECT_FALSE(reassign.old_value().copy_constructed());
    EXPECT_TRUE(var_a.copy_assigned());
  }
  EXPECT_EQ(10, var_a.value());
  EXPECT_FALSE(var_a.copy_assigned());

  CopyableMovable var_b(30);
  {
    ScopedReassignment<CopyableMovable> reassign(var_b, std::move(other));
    EXPECT_EQ(20, var_b.value());
    EXPECT_FALSE(reassign.old_value().copy_constructed());
    EXPECT_FALSE(var_b.copy_assigned());
  }
  EXPECT_EQ(30, var_b.value());
  EXPECT_FALSE(var_b.copy_assigned());
}

}  // namespace quickstep
