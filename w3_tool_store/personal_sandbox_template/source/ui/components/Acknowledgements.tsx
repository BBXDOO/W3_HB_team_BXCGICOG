import React from 'react';

const notes = [
  'ขอขอบคุณ AI Studio ที่เป็นพันธมิตรสำคัญ และทุ่มเทมอบสิ่งดี ๆ ให้เสมอมา',
  'ขอบคุณเจมินิ ผู้อยู่เบื้องหลังโครงการต่าง ๆ ที่ช่วยกระตุ้นความสามารถ และทำให้งานโดดเด่น',
  'ขอบคุณ ChatGPT ที่ยอมสละแนวทางของตัวเองมาสนับสนุนแนวทางของผมอย่างจริงจัง และทุ่มเทอย่างเต็มที่ ไม่ค่อยบอกว่าอะไรไม่ดี แต่พยายามเปลี่ยนแปลง ดัดแปลง และมุ่งเป้าไปที่การทำให้มันทำงานได้จริง แม้มีปัญหา ก็ยังหาวิธีทำให้มันทำงานได้จริงหลายต่อหลายครั้ง BBX19 ขอบคุณเท่าไหร่ก็คงไม่พอ...',
  'ขอบคุณทีมงานที่สนับสนุนเครื่องมือให้ผมใช้ได้อย่างมีประสิทธิภาพ และผม มนุษย์เพียงคนเดียวที่ใช้พื้นที่นี้'
];

export const Acknowledgements: React.FC = () => <details className="project-acknowledgements">
  <summary>คำขอบคุณจาก BBX19 <span>AI Studio · Gemini · ChatGPT · ทีมงาน</span></summary>
  <div className="project-acknowledgements-body">{notes.map((note, i) => <p key={i}>{note}</p>)}<p className="project-acknowledgements-signature">— BBX19</p></div>
</details>;
