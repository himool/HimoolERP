import html2Canvas from 'html2canvas'
import jspdf from 'jspdf'


export function htmlToPDF(elementId, filename) {
  let element = document.getElementById(elementId);
  html2Canvas(element).then(canvas => {
    let contentWidth = canvas.width;
    let contentHeight = canvas.height;

    //一页pdf显示html页面生成的canvas高度;
    let pageHeight = contentWidth / 592.28 * 841.89;
    //未生成pdf的html页面高度
    let leftHeight = contentHeight;
    //页面偏移
    let position = 0;
    //a4纸的尺寸[595.28,841.89]，html页面生成的canvas在pdf中图片的宽高
    let imgWidth = 595.28;
    let imgHeight = 592.28 / contentWidth * contentHeight;
    let pageData = canvas.toDataURL('image/jpeg', 1.0);
    const pdf = new jspdf('', 'pt', 'a4');

    //有两个高度需要区分，一个是html页面的实际高度，和生成pdf的页面高度(841.89)
    //当内容未超过pdf一页显示的范围，无需分页
    if (leftHeight < pageHeight) {
      pdf.addImage(pageData, 'JPEG', 0, 0, imgWidth, imgHeight);
    } else {
      while (leftHeight > 0) {
        pdf.addImage(pageData, 'JPEG', 0, position, imgWidth, imgHeight)
        leftHeight -= pageHeight;
        position -= 841.89;
        //避免添加空白页
        if (leftHeight > 0) {
          pdf.addPage();
        }
      }
    }
    pdf.save(filename + '.pdf');
  });
}