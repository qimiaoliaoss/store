// 获取页面元素
const page1 = document.getElementById("page1");
const page2 = document.getElementById("page2");
const page1Button = document.getElementById("page1Button");
const page2Button = document.getElementById("page2Button");

// 默认显示第一页
page1.style.display = "block";
page2.style.display = "none";

// 点击第一页按钮时显示第一页内容，隐藏第二页内容
page1Button.addEventListener("click", function () {
  page1.style.display = "block";
  page2.style.display = "none";
});

// 点击第二页按钮时显示第二页内容，隐藏第一页内容
page2Button.addEventListener("click", function () {
  page1.style.display = "none";
  page2.style.display = "block";
});

// 当DOM内容加载完毕时，执行以下代码
document.addEventListener("DOMContentLoaded", function () {
  // 获取计算按钮元素
  const calculateButton = document.getElementById("calculateButton");
  // 为计算按钮添加点击事件监听器，点击按钮时触发calculateLateFee函数
  calculateButton.addEventListener("click", calculateLateFee);
});

// 计算滞纳金的函数
function calculateLateFee() {
  // 获取用户输入的日期、本金和滞纳金率
  const dateInput = document.getElementById("dateInput").value;
  const principalInput = parseFloat(document.getElementById("principalInput").value);
  const lateFeeRate = parseFloat(document.getElementById("lateFeeRateInput").value);

  // 将用户输入的日期转换为Date对象，并获取当前日期
  const startDate = new Date(dateInput);
  const currentDate = new Date();
  const dayInMillis = 24 * 60 * 60 * 1000; // 1 day in milliseconds
  const maxLateFeeRate = 1.0; // 100% maximum late fee rate
  const delta = currentDate - startDate + 1

  // 初始化滞纳金和延迟天数
  let lateFee = 0;
  let daysLate = Math.floor(delta / dayInMillis) - 15; // Subtract 15 days as the first 15 days are exempt

  // 如果延迟天数大于0，则计算滞纳金
  if (daysLate > 0) {
    // 计算滞纳金，取滞纳金和本金的100%的较小值
    lateFee = Math.min(principalInput * lateFeeRate * daysLate, principalInput * maxLateFeeRate);
  }

  // 获取结果容器元素，并清空其内容
  const resultContainer = document.getElementById("resultContainer");
  resultContainer.innerHTML = "";

  // 循环计算滞纳金的每一天
  for (let i = 1; i <= daysLate + 1; i++) {
    // 计算当前天的滞纳金金额
    let calculatedLateFee = principalInput * lateFeeRate * i;
    let lateFeeAmount = Math.min(calculatedLateFee, principalInput * maxLateFeeRate);

    // 创建p元素用于显示当天的日期和滞纳金金额
    const dateElement = document.createElement("p");
    // 计算当前天的日期，从开始日期后的第16天开始计算
    const dateOfFee = new Date(startDate.getTime() + (i + 14) * dayInMillis);
    // 设置p元素的文本内容，显示当天日期和滞纳金金额
    dateElement.textContent = dateOfFee.toLocaleDateString() + ": ￥" + lateFeeAmount.toFixed(2);

    // 将p元素添加到结果容器中
    resultContainer.appendChild(dateElement);

    // 如果滞纳金金额已经大于本金，则停止计算
    if (lateFeeAmount >= principalInput) {
      break;
    }
  }
}

function lowertoupper(number, recursive_depth=0) {
  number = number.replace(/[`:_.~!@#$%^&*() \+ =<>?"{}|, \/ ;' \\ [ \] ·~！@#￥%……&*（）—— \+ ={}|《》？：“”【】、；‘’，。、]/g, '');
  let str_number = String(number);
  if (str_number.length > 4) {
    str_number = str_number.slice(-4);
  }

  const bits = "零 一 二 三 四 五 六 七 八 九".split(" ");
  const units = " 十 百 千".split(" ");
  const large_unit = ' 万 亿 万'.split(" ");
  const number_len = str_number.length;
  let result = "";

  for (let i = 0; i < number_len; i++) {
    result += bits[parseInt(str_number[i])];
    if (str_number[i] !== "0") {
      result += units[number_len - i - 1];
    }
  }

  // 去除连续的零
  while (result.includes("零零")) {
    result = result.replace("零零", "零");
  }
  // 去除尾部的零
  if (result.slice(-1) === "零") {
    result = result.slice(0, -1);
  }
  // 调整10~20之间的数
  if (result.slice(0, 2) === "一十") {
    result = result.slice(1);
  }
  // 字符串连接上大单位
  result += large_unit[recursive_depth];

  // 判断是否递归
  if (String(number).length > 4) {
    recursive_depth++;
    return lowertoupper(String(number).slice(0, -4), recursive_depth) + result;
  } else {
    return result;
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const convertButton = document.getElementById("convertButton_2");
  convertButton.addEventListener("click", convertNumber);
});

function convertNumber() {
  const numberInput = document.getElementById("numberInput").value;
  const convertedNumber = lowertoupper(numberInput);

  const resultContainer = document.getElementById("resultContainer_2");
  resultContainer.innerHTML = "转换结果：" + convertedNumber;
}
