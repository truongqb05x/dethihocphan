-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: localhost:3306
-- Thời gian đã tạo: Th2 20, 2025 lúc 08:29 PM
-- Phiên bản máy phục vụ: 10.6.19-MariaDB-cll-lve-log
-- Phiên bản PHP: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `mmddllg_huehub`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `departments_group`
--

CREATE TABLE `departments_group` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `documents`
--

CREATE TABLE `documents` (
  `id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `year` varchar(20) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_info` varchar(255) NOT NULL,
  `document_type` enum('exam','syllabus') NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `documents`
--

INSERT INTO `documents` (`id`, `subject_id`, `year`, `file_name`, `file_info`, `document_type`, `file_path`, `created_at`, `updated_at`) VALUES
(2, 54, '2022 - 2023', 'Cơ Sở Toán', 'Trường Đại học Khoa học - Khoa Toán - Môn Cơ Sở Toán - 2022 - 2023', 'exam', 'static/exams/462570060_956417796406782_2378835644355054276_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(3, 34, '2022 - 2023', 'Mạng Máy Tính', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Mạng Máy Tính - 2022 - 2023', 'exam', 'static/exams/BO4TZ8PU_bb0de3c7-a2ff-4dda-8622-ca91065c4b27.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(4, 24, '2023 - 2024', 'Font End', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Font End - 2023 - 2024', 'exam', 'static/exams/465196139_1783982829088573_7730726195714248052_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(5, 6, '2022 - 2023', 'Môi Trường Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Môi Trường Đại Cương - 2022 - 2023', 'exam', 'static/exams/385525005_360907463012640_943294502171450229.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(6, 20, '2022 - 2023', 'Triết Học Mác', 'Trường Đại học Khoa học - Môn học đại cương - Môn Triết Học Mác - 2022 - 2023', 'exam', 'static/exams/370257338_856555482870773_8579671780738823490.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(7, 25, '2023 - 2024', 'Hướng Đối Tượng', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Hướng Đối Tượng - 2023 - 2024', 'exam', 'static/exams/6c8b4665-6943-462f-a1d7-560b9cc1de9f.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(8, 55, '2022 - 2023', 'Giải Tích', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2022 - 2023', 'exam', 'static/exams/Q3NVTAQZ_gt11.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(9, 14, '2023 - 2024', 'Xã Hội Học Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Xã Hội Học Đại Cương - 2023 - 2024', 'exam', 'static/exams/KY3OOVIG_42d7e4bd-b31e-4ddd-98a8-6bfed3d0353c.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(10, 9, '2022 - 2023', 'Pháp Luật Việt Nam Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Pháp Luật Việt Nam Đại Cương - 0', 'exam', 'static/exams/VOMIZHMH_176caf13-ada4-471c-b7dd-fb830e75966a.jpg', '2025-02-20 03:34:30', '2025-02-20 10:57:59'),
(11, 19, '2023 - 2024', 'Kinh Tế Chính Trị Mác', 'Trường Đại học Khoa học - Môn học đại cương - Môn Kinh Tế Chính Trị Mác - 2023 - 2024', 'exam', 'static/exams/VIGVOMIZ_59d1fb17-a010-49e0-aac8-a870605512c4.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(12, 50, '2023 - 2024', 'Sáng Tạo Nội Dung Truyền Thông', 'Trường Đại học Khoa học - Khoa Báo chí - Truyền thông - Môn Sáng Tạo Nội Dung Truyền Thông - 0', 'exam', 'static/exams/HMH5ZJI9_a0e41202-2959-48d0-9637-1a19d0e1a5ef.jpg', '2025-02-20 03:34:30', '2025-02-20 10:55:49'),
(13, 156, '2023 - 2024', 'Lịch Sử Văn Minh Thế Giới', 'Trường Đại học Khoa học - Khoa Lịch sử - Môn Lịch Sử Văn Minh Thế Giới - 0', 'exam', 'static/exams/X50BB75H_4b2f7c37-f493-4677-a6ff-548dc55cd5a1.jpg', '2025-02-20 03:34:30', '2025-02-20 10:58:34'),
(14, 49, '2023 - 2024', 'Quản Trị Truyền Thông Trong Khủng Hoảng', 'Trường Đại học Khoa học - Khoa Báo chí - Truyền thông - Môn Quản Trị Truyền Thông Trong Khủng Hoảng - 0', 'exam', 'static/exams/5K8CRXJ2_ff4fabf6-2e0c-4742-b924-3220fde13648.jpg', '2025-02-20 03:34:30', '2025-02-20 10:59:06'),
(15, 16, '2023 - 2024', 'Chủ Nghĩa Xã Hội Khoa Học', 'Trường Đại học Khoa học - Môn học đại cương - Môn Chủ Nghĩa Xã Hội Khoa Học - 2023 - 2024', 'exam', 'static/exams/DBJ7NJB4_c6f190f5-ec83-406b-804b-cc589309be73.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(16, 7, '2023 - 2024', 'Mỹ Học Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Mỹ Học Đại Cương - 2023 - 2024', 'exam', 'static/exams/BFKBS8A1_ab5e1b45-8ee3-43d9-8e88-4d4d724f476c.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(17, 36, '2022 - 2023', 'Nhập Môn Cơ Sở Dữ Liệu', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nhập Môn Cơ Sở Dữ Liệu - 2022 - 2023', 'exam', 'static/exams/60F280BO_368022238_203209676158436_8914474545062526475.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(18, 55, '2023 - 2024', 'Giải Tích', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2023 - 2024', 'exam', 'static/exams/Q3NVTAQZ_gt2.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(19, 63, '2023 - 2024', 'Đại Số Tuyến Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Đại Số Tuyến Tính - 2023 - 2024', 'exam', 'static/exams/C3A4VLIW_440840512_464247812844647_347560182441659478_n.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(20, 34, '2023 - 2024', 'Mạng Máy Tính', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Mạng Máy Tính - 2023 - 2024', 'exam', 'static/exams/OAK8MQQ0_a05c0235-81f2-49da-86c5-47cea21e86ec.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(21, 55, '2022 - 2023', 'Giải Tích 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2022 - 2023', 'exam', 'static/exams/Q3NVTAQZ_gt.pdf', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(22, 28, '0', 'Kiến Trúc Máy Tính', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Kiến Trúc Máy Tính - 0', 'exam', 'static/exams/3BJKNKBV_387476878_250426621046331_7388340409573828859_n (1).jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(23, 61, '2023 - 2024', 'Toán Rời Rạc', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2023 - 2024', 'exam', 'static/exams/SS60F280_452638669_367953762997281_1121871179225113087_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(24, 114, '2022 - 2023', 'Cấu Trúc Dữ Liệu và Thuật Toán', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Cấu Trúc Dữ Liệu và Thuật Toán - 2022 - 2023', 'exam', 'static/exams/BO4TZ8PU_452638669_367953762997281_1121871179225113087_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(25, 40, '2022-2023', 'Python', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Python - 2022-2023', 'exam', 'static/exams/60F280BO_dethi_so1_luot2.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(26, 62, '2022 - 2023', 'Xác Xuất Thống Kê', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2022 - 2023', 'exam', 'static/exams/SS60F280_447027773_333329946459663_8368781502667063764_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(27, 26, '2022 - 2023', 'Java Cơ Bản', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Java Cơ Bản - 2022 - 2023', 'exam', 'static/exams/1X4ADYZB_445687114_333330126459645_4706438088711658406_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(28, 41, '2022 - 2023', 'Thiết Kế Cơ Sở Dữ Liệu', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Thiết Kế Cơ Sở Dữ Liệu - 2022 - 2023', 'exam', 'static/exams/BO4TZ8PU_447305934_334643582994966_644284662783052633_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(29, 108, '2023 - 2024', 'Hình Học Họa Hình 1', 'Trường Đại học Khoa học - Khoa Kiến trúc - Môn Hình Học Họa Hình 1 - 2023 - 2024', 'exam', 'static/exams/U5OE11O3_363bd1a0-41ad-46fd-80f2-eada8cf64ff3.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(30, 109, '2023 - 2024', 'Hình Học Họa Hình 2', 'Trường Đại học Khoa học - Khoa Kiến trúc - Môn Hình Học Họa Hình 2 - 2023 - 2024', 'exam', 'static/exams/V60ULX31_7aea1970-ddd7-4d59-bc80-44840ac5aecd.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(31, 35, '2023 - 2024', 'Nguyên Lí Hệ Điều Hành', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nguyên Lí Hệ Điều Hành - 2023 - 2024', 'exam', 'static/exams/SS60F280_4e633937-93a0-4d1a-93a2-825d99ea3560.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(32, 57, '2023 - 2024', 'Phương Pháp Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Pháp Tính - 2023 - 2024', 'exam', 'static/exams/HP80BKEG_446873870_333330313126293_4162822353174843708_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(33, 40, '2023-2024', 'Python', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Python - 2023-2024', 'exam', 'static/exams/SS60F280_DeThi_2.docx.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(34, 25, '2022-2023', 'Hướng Đối Tượng', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Hướng Đối Tượng - 2022-2023', 'exam', 'static/exams/O4TZ8PUU_hdt2.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(35, 25, '2021-2022', 'Hướng Đối Tượng', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Hướng Đối Tượng - 2021-2022', 'exam', 'static/exams/BKEG31H0_hdt.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(36, 37, '2021 - 2022', 'Nhập Môn Lập Trình', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nhập Môn Lập Trình - 2021 - 2022', 'exam', 'static/exams/SS60F280_393912726_319774580874879_7274836505302827411_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(37, 30, '2023 - 2024', 'Kỹ Thuật Lập Trình', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Kỹ Thuật Lập Trình - 2023 - 2024', 'exam', 'static/exams/Q3NVTAQZ_b0162.vi.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(38, 31, '2023 - 2024', 'Lập Trình Nâng Cao', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Lập Trình Nâng Cao - 2023 - 2024', 'exam', 'static/exams/1Q2BOXOB_pb0161.v.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(39, 37, '2023 - 2024', 'Nhập Môn Lập Trình Hè', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nhập Môn Lập Trình - 0', 'exam', 'static/exams/Q3NVTAQZ_olpicpc031c08c.vpdf.pdf', '2025-02-20 03:34:30', '2025-02-20 11:00:11'),
(40, 61, '2024 - 2025', 'Toán Rời Rạc', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2024 - 2025', 'exam', 'static/exams/8X1BX8KL_f446619a-c1fe-4a77-806d-3862c5a01ae9.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(41, 155, '2022 - 2023', 'Logic Học', 'Trường Đại học Khoa học - Khoa Lý luận chính trị - Môn Logic Học - 2022 - 2023', 'exam', 'static/exams/DK06XZIH_8f9d198d-81b1-4871-bb81-75f1ab2c46bb.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(42, 157, '2022 - 2023', 'Phương Pháp Luận Nghiên Cứu Khoa Học', 'Trường Đại học Khoa học - Khoa Xã hội học và Công tác xã hội - Môn Phương Pháp Luận Nghiên Cứu Khoa Học - 2022 - 2023', 'exam', 'static/exams/QBLQEZFS_9b2e9f2c-3bbe-41f1-9250-c548ff6742ef.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(43, 80, '2023 - 2024', 'Văn Hóa Huế', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Văn Hóa Huế - 2023 - 2024', 'exam', 'static/exams/4EGLY7GT_1aec9cab-5204-42cd-8f4a-0b4858228e3f.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(44, 67, '2023 - 2024', 'Các Hướng Tiếp Cận Tác Phẩm Văn Học Chương Trình Phổ Thông', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Các Hướng Tiếp Cận Tác Phẩm Văn Học Chương Trình Phổ Thông - 2023 - 2024', 'exam', 'static/exams/DK06XZIH_34e89267-4fd0-49e2-9801-e97f4359540a.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(45, 84, '2023 - 2024', 'Tổng Quan Văn Học Phương Tây', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Tổng Quan Văn Học Phương Tây - 2023 - 2024', 'exam', 'static/exams/QBLQEZFS_12a223f5-f205-4f21-9598-469f2a4f5993.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(46, 83, '2023 - 2024', 'Văn Học Việt Nam Hiện Đại', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Văn Học Việt Nam Hiện Đại - 2023 - 2024', 'exam', 'static/exams/4EGLY7GT_02d42398-123c-4bb5-aa1e-e4daeb5b1202.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(47, 68, '2023 - 2024', 'Cơ Sở Việt Ngữ Học', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Cơ Sở Việt Ngữ Học - 2023 - 2024', 'exam', 'static/exams/C83MR0R4_35af0b35-7179-450d-8f53-baa9f08f4d96.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(48, 81, '2023 - 2024', 'Văn Hóa Và Văn Học Ấn Độ - Đông Nam Á', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Văn Hóa Và Văn Học Ấn Độ - Đông Nam Á - 2023 - 2024', 'exam', 'static/exams/DK06XZIH_00068e3d-1b9d-47a6-a2a5-fb9fb23d4521.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(49, 77, '2023 - 2024', 'Tiếp Nhận Văn Học', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Tiếp Nhận Văn Học - 2023 - 2024', 'exam', 'static/exams/QBLQEZFS_f3373bf0-9a05-4d69-88d9-5060c2e20957.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(50, 0, '2023 - 2024', 'Lịch Sử Đảng Việt Nam', '', 'exam', 'static/exams/4EGLY7GT_a636c1e4-66fd-465e-be1e-3038c04802b2.jpg', '2025-02-20 03:34:30', '2025-02-20 05:04:26'),
(51, 16, '2023 - 2024', 'Chủ Nghĩa Xã Hội Khoa Học 1', 'Trường Đại học Khoa học - Môn học đại cương - Môn Chủ Nghĩa Xã Hội Khoa Học - 2023 - 2024', 'exam', 'static/exams/C83MR0R4_bc83a838-5bb7-46de-93a6-6178945b457f.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(52, 78, '2023 - 2024', 'Tác Phẩm Và Thể Loại Văn Học', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Tác Phẩm Và Thể Loại Văn Học - 2023 - 2024', 'exam', 'static/exams/016N9SDO_282daea2-4b5b-4ba7-af07-55511bce7784.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(53, 79, '2023 - 2024', 'Tổng Quan Văn Học Phương Đông', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Tổng Quan Văn Học Phương Đông - 2023 - 2024', 'exam', 'static/exams/Y2WP7UXJ_55a9713d-c1fb-4d80-8723-2e13ed59cf92.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(54, 76, '2023 - 2024', 'Tiếng Việt Thực Hành', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Tiếng Việt Thực Hành - 2023 - 2024', 'exam', 'static/exams/KWQ3IBCU_4d7ec4ca-c1ca-4b0a-90f2-81613111b0da.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(55, 19, '2022 - 2023', 'Kinh Tế Chính Trị Mác', 'Trường Đại học Khoa học - Môn học đại cương - Môn Kinh Tế Chính Trị Mác - 2022 - 2023', 'exam', 'static/exams/DK06XZIH_33afb7f8-a6be-4330-b9ba-94c0b396ad33.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(56, 70, '2022 - 2023', 'Ngôn Ngữ Học', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Ngôn Ngữ Học - 2022 - 2023', 'exam', 'static/exams/DK06XZIH_b4c23eb5-bd1a-434f-905d-08c1d2e1e23e.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(57, 72, '2022 - 2023', 'Nhập Môn Lí Luận Văn Học', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Nhập Môn Lí Luận Văn Học - 2022 - 2023', 'exam', 'static/exams/QBLQEZFS_0920473a-f796-4276-b9b7-4b6343392e48.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(58, 82, '2022 - 2023', 'Văn Học Dân Gian', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Văn Học Dân Gian - 2022 - 2023', 'exam', 'static/exams/QBLQEZFS_bb541b78-e100-4f4a-bc86-d977203855d2.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(59, 9, '2022 - 2023', 'Pháp Luật Việt Nam Đại Cương 1', 'Trường Đại học Khoa học - Môn học đại cương - Môn Pháp Luật Việt Nam Đại Cương - 0', 'exam', 'static/exams/0NRHF2SI_25cd49cb-2ac6-4a41-99c9-1dc087b1b850.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(60, 57, '2017 - 2018', 'Phương Pháp Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Pháp Tính - 2017 - 2018', 'exam', 'static/exams/NP6RRQMQ_448251544_341284432330881_5868132761011729312_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(61, 28, '0', 'Bộ đề vấn đáp kiến trúc máy tính', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Kiến Trúc Máy Tính - 0', 'syllabus', 'static/exams/U1AFZWRE_BoDeVanDap_KTMT_HK2_2021-2022.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(62, 0, '0', 'Đề cương ôn tập Pháp Luật Đại Cương', '', 'syllabus', 'static/exams/YGHFYYTX_pldc.docx', '2025-02-20 03:34:30', '2025-02-20 03:36:28'),
(63, 45, '2023-2024', 'SQL', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn SQL - 2023-2024', 'exam', 'static/exams/EWOIRPUY_sql.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(64, 20, '0', '13 Câu Ôn Tập Triết Học Mác', 'Trường Đại học Khoa học - Môn học đại cương - Môn Triết Học Mác - 0', 'syllabus', 'static/exams/A1XULLDA_trietsss.docx', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(65, 0, '0', 'Đề cương học phần Lịch Sử Báo Chí Thế Giới', '', 'syllabus', 'static/exams/I5SDF385_dclstg.docx', '2025-02-20 03:34:30', '2025-02-20 03:36:28'),
(66, 156, '0', 'Đề cương học phần Lịch Sử Văn Minh Thế Giới', 'Trường Đại học Khoa học - Khoa Lịch sử - Môn Lịch Sử Văn Minh Thế Giới - 0', 'syllabus', 'static/exams/I5SDF385_lsvmtg.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(67, 48, '0', 'Đề cương học phần Lịch Sử Báo Chí Việt Nam', 'Trường Đại học Khoa học - Khoa Báo chí - Truyền thông - Môn Lịch Sử Báo Chí Việt Nam - 0', 'syllabus', 'static/exams/385GTLHS_bcvn.docx', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(68, 0, '0', 'Đề cương học phần Tâm Lý Học', '', 'syllabus', 'static/exams/YSR3OLZU_tamlyhoc.docx', '2025-02-20 03:34:30', '2025-02-20 03:36:28'),
(69, 19, '0', 'Đề cương học phần Kinh Tế Chính Trị Mác', 'Trường Đại học Khoa học - Môn học đại cương - Môn Kinh Tế Chính Trị Mác - 0', 'syllabus', 'static/exams/3QU9GQV0_ktct.docx', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(70, 42, '2022 - 2023', 'Thiết Kế Đồ Hoạ Ứng Dụng', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Thiết Kế Đồ Hoạ Ứng Dụng - 2022 - 2023', 'exam', 'static/exams/YSR3OLZU_73c09e94-7a9f-41a8-810e-d8eceb7be62c.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(71, 24, '2023 - 2024', 'Font End 1', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Font End - 2023 - 2024', 'exam', 'static/exams/AAP9D098_448103342_377638395323719_2986520842588417092_n.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(72, 61, '2014 - 2015', 'Toán Rời Rạc', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2014 - 2015', 'exam', 'static/exams/AAP9D098_8ad1cbec-b11b-4d9b-8617-47cabd1135fc.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(73, 61, '2006 - 2007', 'Toán Rời Rạc', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2006 - 2007', 'exam', 'static/exams/AAP9D098_8c9d406b-7de6-49d5-8cdb-ec102b679cbd.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(74, 61, '2015 - 2016', 'Toán Rời Rạc', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2015 - 2016', 'exam', 'static/exams/Z4JQ9U9A_afb649ed-8dbc-4f89-b1fc-d13b50e5bac5.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(75, 61, '2011 - 2012', 'Toán Rời Rạc', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2011 - 2012', 'exam', 'static/exams/Z4JQ9U9A_f6a8bbcb-afe1-4725-9c0b-30b09b0038e0.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(76, 61, '2015 - 2016', 'Toán Rời Rạc 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2015 - 2016', 'exam', 'static/exams/JNFR2JBC_d9bc8b7b-9d19-4fd5-bf46-31b08d5c3335.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(77, 61, '2017 - 2018', 'Toán Rời Rạc', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2017 - 2018', 'exam', 'static/exams/9BTAS4WQ_1ef1effa-7373-47b0-a0c5-d0af0452611d.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(78, 61, '2013 - 2014', 'Toán Rời Rạc', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2013 - 2014', 'exam', 'static/exams/XTQ0JMEL_7d4e6f5d-76d4-4526-9f1b-f68db278da9b.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(79, 25, '2023 - 2024', 'Hướng Đối Tượng 1', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Hướng Đối Tượng - 2023 - 2024', 'exam', 'static/exams/JNFR2JBC_33a247be-0c08-4a8d-b0ed-4b23edd9bf30.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(80, 26, '2022 - 2023', 'Java Cơ Bản 1', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Java Cơ Bản - 2022 - 2023', 'exam', 'static/exams/9BTAS4WQ_446951396_333330026459655_1820664361080830402_n.pdf', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(81, 57, '2013 - 2014', 'Phương Pháp Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Pháp Tính - 2013 - 2014', 'exam', 'static/exams/4OR7ZJNH_448312169_341283678997623_5957736616705520262_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(82, 57, '2011 - 2012', 'Phương Pháp Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Pháp Tính - 2011 - 2012', 'exam', 'static/exams/DJ8I34UK_448166940_341284132330911_3235041744019611221_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(83, 57, '2010 - 2011', 'Phương Pháp Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Pháp Tính - 2010 - 2011', 'exam', 'static/exams/HHI4OAC6_448310654_341284178997573_3931025677027333085_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(84, 57, '2014 - 2015', 'Phương Pháp Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Pháp Tính - 2014 - 2015', 'exam', 'static/exams/AAP9D098_448252855_341284495664208_6539330582802416272_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(85, 57, '2010 - 2011', 'Phương Pháp Tính 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Pháp Tính - 2010 - 2011', 'exam', 'static/exams/TTAHADQU_448215648_341284675664190_5086404789743322592_n.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(86, 57, '2010 - 2011', 'Phương Pháp Tính 2', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Pháp Tính - 2010 - 2011', 'exam', 'static/exams/SN7B4ZVS_448316313_341284715664186_3452250596792869946_n.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(87, 57, '2011 - 2012', 'Phương Pháp Tính 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Pháp Tính - 2011 - 2012', 'exam', 'static/exams/HC245NHV_448247182_341284758997515_2058288767686767447_n.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(88, 57, '2009 - 2010', 'Phương Pháp Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Pháp Tính - 2009 - 2010', 'exam', 'static/exams/CZ78TUEC_448266246_341283355664322_3394171637057681382_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(89, 57, '2011 - 2012', 'Phương Pháp Tính 2', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Pháp Tính - 2011 - 2012', 'exam', 'static/exams/Z4JQ9U9A_448087229_341283428997648_8386837015941301243_n.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(90, 57, '2009 - 2010', 'Phương Pháp Tính 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Pháp Tính - 2009 - 2010', 'exam', 'static/exams/JNFR2JBC_448211192_341283515664306_7214163622791032818_n.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(91, 33, '2022 - 2023', 'Mô Hình Hóa UML', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Mô Hình Hóa UML - 2022 - 2023', 'exam', 'static/exams/I7GR415D_448160873_341864492272875_3168153095923858822_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(92, 44, '2015 - 2016', 'Đồ Họa Máy Tính', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Đồ Họa Máy Tính - 2015 - 2016', 'exam', 'static/exams/9BTAS4WQ_452669138_367953586330632_2939716135662094101_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(93, 44, '2013 - 2014', 'Đồ Họa Máy Tính', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Đồ Họa Máy Tính - 2013 - 2014', 'exam', 'static/exams/XTQ0JMEL_452615846_367953619663962_8709989238179052187_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(94, 44, '2016 - 2017', 'Đồ Họa Máy Tính', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Đồ Họa Máy Tính - 2016 - 2017', 'exam', 'static/exams/4OR7ZJNH_452552610_367953646330626_8029024917984518647_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(95, 55, '2022 - 2023', 'Giải Tích 2', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2022 - 2023', 'exam', 'static/exams/JJJRE916_452533535_367953676330623_3263578549008109382_n.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(96, 55, '2024 -2025', 'Đề thi giữa kì học phần Giải Tích', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2024 -2025', 'exam', 'static/exams/DJ8I34UK_452699674_367953712997286_8685801302253659636_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(97, 54, '2014 - 2015', 'Cơ Sở Toán', 'Trường Đại học Khoa học - Khoa Toán - Môn Cơ Sở Toán - 2014 - 2015', 'exam', 'static/exams/DB3SBE0H_453042957_369899999469324_7474792507360560670_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(98, 54, '2015 - 2016', 'Cơ Sở Toán', 'Trường Đại học Khoa học - Khoa Toán - Môn Cơ Sở Toán - 2015 - 2016', 'exam', 'static/exams/C21I0AO0_453042983_369900162802641_3084054759252267790_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(99, 54, '2015 - 2016', 'Cơ Sở Toán 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Cơ Sở Toán - 2015 - 2016', 'exam', 'static/exams/QM0BYB7A_453045795_369900212802636_5148553682036122543_n.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(100, 54, '2016 - 2017', 'Cơ Sở Toán', 'Trường Đại học Khoa học - Khoa Toán - Môn Cơ Sở Toán - 2016 - 2017', 'exam', 'static/exams/8K096M4C_453043742_369900446135946_1277179447627455919_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(101, 54, '2016 - 2017', 'Cơ Sở Toán 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Cơ Sở Toán - 2016 - 2017', 'exam', 'static/exams/J62I46Y6_453039211_369900496135941_4361375199694943585_n.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(102, 54, '2017 - 2018', 'Cơ Sở Toán', 'Trường Đại học Khoa học - Khoa Toán - Môn Cơ Sở Toán - 2017 - 2018', 'exam', 'static/exams/UPKGO50I_453037143_369900549469269_5037061723041948462_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(103, 54, '2017 - 2018', 'Cơ Sở Toán Hè', 'Trường Đại học Khoa học - Khoa Toán - Môn Cơ Sở Toán - 2017 - 2018', 'exam', 'static/exams/GGC9T6BQ_453046399_369900579469266_690706807894470_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(104, 54, '2018 - 2019', 'Cơ Sở Toán', 'Trường Đại học Khoa học - Khoa Toán - Môn Cơ Sở Toán - 2018 - 2019', 'exam', 'static/exams/G7LMIC5P_452994643_369900632802594_5543731378590554329_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(105, 54, '2013 - 2014', 'Cơ Sở Toán', 'Trường Đại học Khoa học - Khoa Toán - Môn Cơ Sở Toán - 2013 - 2014', 'exam', 'static/exams/DJH4XV5B_453262278_369900676135923_1219138863522167194_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(106, 28, '2022 - 2023', 'Kiến Trúc Máy Tính', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Kiến Trúc Máy Tính - 2022 - 2023', 'exam', 'static/exams/3C6MWJ4T_454912753_379068745219116_2704363773864361651_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(107, 28, '2022 - 2023', 'Kiến Trúc Máy Tính 1', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Kiến Trúc Máy Tính - 2022 - 2023', 'exam', 'static/exams/Z4JQ9U9A_454805964_379067405219250_3688266494832388946_n.pdf', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(108, 43, '2023 - 2024', 'Trí Tuệ Nhân Tạo', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Trí Tuệ Nhân Tạo - 2023 - 2024', 'exam', 'static/exams/9HIUA7ZN_468037113_452375707888419_7525895540229651778_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(109, 16, '0', 'Đề Cương Chủ Nghĩa Xã Hội Khoa Học', 'Trường Đại học Khoa học - Môn học đại cương - Môn Chủ Nghĩa Xã Hội Khoa Học - 0', 'syllabus', 'static/exams/JQ8KDTV6_a.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(110, 0, '0', 'Đề Cương Lịch Sử Đảng', '', 'syllabus', 'static/exams/JNFR2JBC_c.docx', '2025-02-20 03:34:30', '2025-02-20 03:36:28'),
(111, 18, '0', 'NGÂN HÀNG ĐỀ THI KẾT THÚC HỌC PHẦN Tư Tưởng HCM', 'Trường Đại học Khoa học - Môn học đại cương - Môn Tư Tưởng HCM - 0', 'syllabus', 'static/exams/9BTAS4WQ_tt.docx.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(112, 62, '2013 - 2014', 'Xác Xuất Thống Kê', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2013 - 2014', 'exam', 'static/exams/YZAQC06G_68945174_333166127637441_3909428517292474368_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(113, 62, '2015 - 2016', 'Xác Xuất Thống Kê', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2015 - 2016', 'exam', 'static/exams/YZAQC06G_67834869_333165967637457_3739934921515335680_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(114, 62, '2016 - 2017', 'Xác Xuất Thống Kê', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2016 - 2017', 'exam', 'static/exams/47QV562K_67871824_333165874304133_5249284990239244288_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(115, 62, '2018 - 2019', 'Xác Xuất Thống Kê', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2018 - 2019', 'exam', 'static/exams/UT32T8X1_68498403_333166184304102_3626312433578016768_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(116, 62, '2016 - 2017', 'Xác Xuất Thống Kê 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2016 - 2017', 'exam', 'static/exams/SAS68UD3_67872022_333166244304096_5906486313049128960_n.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(117, 57, '2018 - 2019', 'Phương Pháp Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Pháp Tính - 2018 - 2019', 'exam', 'static/exams/47QV562K_81230026_1007990136200520_7199069622862086144_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(118, 35, '2011 - 2012', 'Nguyên Lí Hệ Điều Hành', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nguyên Lí Hệ Điều Hành - 2011 - 2012', 'exam', 'static/exams/UT32T8X1_23052014871pdf.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(119, 41, '2012 - 2013', 'Thiết Kế Cơ Sở Dữ Liệu', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Thiết Kế Cơ Sở Dữ Liệu - 2012 - 2013', 'exam', 'static/exams/SAS68UD3_23052014873.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(120, 33, '2013 - 2014', 'Mô Hình Hóa UML', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Mô Hình Hóa UML - 2013 - 2014', 'exam', 'static/exams/KALC2RSN_23052014994.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(121, 41, '2010 - 2011', 'Thiết Kế Cơ Sở Dữ Liệu', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Thiết Kế Cơ Sở Dữ Liệu - 2010 - 2011', 'exam', 'static/exams/COCQPIVN_23052014992.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(122, 41, '2011 - 2012', 'Thiết Kế Cơ Sở Dữ Liệu', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Thiết Kế Cơ Sở Dữ Liệu - 2011 - 2012', 'exam', 'static/exams/YZAQC06G_23052014991.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(123, 44, '2011 - 2012', 'Đồ Họa Máy Tính', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Đồ Họa Máy Tính - 2011 - 2012', 'exam', 'static/exams/RBZUGIN5_23052014990.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(124, 44, '2011 - 2012', 'Đồ Họa Máy Tính 1', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Đồ Họa Máy Tính - 2011 - 2012', 'exam', 'static/exams/IV4CHOQD_23052014989.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(125, 44, '2011 - 2012', 'Đồ Họa Máy Tính 2', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Đồ Họa Máy Tính - 2011 - 2012', 'exam', 'static/exams/YZAQC06G_23052014988.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(126, 29, '0', 'Kỹ Nghệ Phần Mềm', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Kỹ Nghệ Phần Mềm - 0', 'exam', 'static/exams/STGN9TPF_23052014987.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(127, 44, '2010 - 2011', 'Đồ Họa Máy Tính', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Đồ Họa Máy Tính - 2010 - 2011', 'exam', 'static/exams/U8EQW8A7_23052014986.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(128, 44, '2010 - 2011', 'Đồ Họa Máy Tính 1', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Đồ Họa Máy Tính - 2010 - 2011', 'exam', 'static/exams/47QV562K_23052014985.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(129, 38, '2011 - 2012', 'Nhập Môn Trí Tuệ Nhân Tạo', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nhập Môn Trí Tuệ Nhân Tạo - 2011 - 2012', 'exam', 'static/exams/9Y6R45TQ_23052014983.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(130, 29, '2011 - 2012', 'Kỹ Nghệ Phần Mềm', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Kỹ Nghệ Phần Mềm - 2011 - 2012', 'exam', 'static/exams/UT32T8X1_23052014982.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(131, 12, '0', 'Vật Lý Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Vật Lý Đại Cương - 0', 'exam', 'static/exams/SAS68UD3_23052014981.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(132, 114, '2012 - 2013', 'Cấu Trúc Dữ Liệu và Thuật Toán', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Cấu Trúc Dữ Liệu và Thuật Toán - 2012 - 2013', 'exam', 'static/exams/LUAYRATS_23052014979.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(133, 23, '0', 'Công Nghệ Phần Mềm', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Công Nghệ Phần Mềm - 0', 'exam', 'static/exams/47QV562K_23052014978.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(134, 59, '2012 - 2013', 'Phép Tính Tích Phân Và Hàm Nhiều Biến', 'Trường Đại học Khoa học - Khoa Toán - Môn Phép Tính Tích Phân Và Hàm Nhiều Biến - 2012 - 2013', 'exam', 'static/exams/K27HJS8V_23052014974.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(135, 32, '0', 'Lý Thuyết Đồ Họa', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Lý Thuyết Đồ Họa - 0', 'exam', 'static/exams/GBZNT1KB_23052014973.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(136, 29, '2011 - 2012', 'Kỹ Nghệ Phần Mềm 1', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Kỹ Nghệ Phần Mềm - 2011 - 2012', 'exam', 'static/exams/UT32T8X1_23052014971.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(137, 34, '2012 - 2013', 'Mạng Máy Tính', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Mạng Máy Tính - 2012 - 2013', 'exam', 'static/exams/SAS68UD3_23052014970.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(138, 22, '2009 - 2013', 'Các Hệ Quản Trị CSDL', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Các Hệ Quản Trị CSDL - 2009 - 2013', 'exam', 'static/exams/KALC2RSN_23052014969.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(139, 59, '2012 - 2013', 'Phép Tính Tích Phân Và Hàm Nhiều Biến 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Phép Tính Tích Phân Và Hàm Nhiều Biến - 2012 - 2013', 'exam', 'static/exams/V7Z1LZQY_23052014968.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(140, 59, '2010 - 2011', 'Phép Tính Tích Phân Và Hàm Nhiều Biến', 'Trường Đại học Khoa học - Khoa Toán - Môn Phép Tính Tích Phân Và Hàm Nhiều Biến - 2010 - 2011', 'exam', 'static/exams/COCQPIVN_23052014967.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(141, 59, '2009 - 2010', 'Phép Tính Tích Phân Và Hàm Nhiều Biến', 'Trường Đại học Khoa học - Khoa Toán - Môn Phép Tính Tích Phân Và Hàm Nhiều Biến - 2009 - 2010', 'exam', 'static/exams/RBZUGIN5_23052014966.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(142, 59, '2011 - 2012', 'Phép Tính Tích Phân Và Hàm Nhiều Biến', 'Trường Đại học Khoa học - Khoa Toán - Môn Phép Tính Tích Phân Và Hàm Nhiều Biến - 2011 - 2012', 'exam', 'static/exams/YZAQC06G_23052014965.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(143, 12, '2012 - 2013', 'Vật Lý Đại Cương Kì Hè', 'Trường Đại học Khoa học - Môn học đại cương - Môn Vật Lý Đại Cương - 2012 - 2013', 'exam', 'static/exams/IV4CHOQD_23052014953.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(144, 61, '2007 - 2008', 'Toán Rời Rạc', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2007 - 2008', 'exam', 'static/exams/ZLKUB2EU_23052014951.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(145, 54, '2010 - 2011', 'Cơ Sở Toán', 'Trường Đại học Khoa học - Khoa Toán - Môn Cơ Sở Toán - 2010 - 2011', 'exam', 'static/exams/9K6XAYA8_23052014944.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(146, 135, '2011 - 2012', 'Cách Mạng Của Đảng Cộng Sản Việt Nam', 'Trường Đại học Khoa học - Khoa Lý luận chính trị - Môn Cách Mạng Của Đảng Cộng Sản Việt Nam - 2011 - 2012', 'exam', 'static/exams/QYAIJD3Y_23052014932.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(147, 62, '2011 - 2012', 'Xác Xuất Thống Kê', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2011 - 2012', 'exam', 'static/exams/X8KLGIPO_23052014931.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(148, 36, '2012 - 2013', 'Nhập Môn Cơ Sở Dữ Liệu', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nhập Môn Cơ Sở Dữ Liệu - 2012 - 2013', 'exam', 'static/exams/YZAQC06G_23052014929.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(149, 61, '2012 - 2013', 'Toán Rời Rạc', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2012 - 2013', 'exam', 'static/exams/47QV562K_23052014927.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(150, 25, '2012-2013', 'Hướng Đối Tượng', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Hướng Đối Tượng - 2012-2013', 'exam', 'static/exams/UT32T8X1_23052014921.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(151, 61, '2012 - 2013', 'Toán Rời Rạc 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2012 - 2013', 'exam', 'static/exams/O84RYFYM_23052014916.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(152, 39, '2011 - 2012', 'Phân Tích Hệ Thống Thông Tin', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Phân Tích Hệ Thống Thông Tin - 2011 - 2012', 'exam', 'static/exams/O84RYFYM_23052014915.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(153, 62, '2010 - 2011', 'Xác Xuất Thống Kê', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2010 - 2011', 'exam', 'static/exams/O84RYFYM_23052014904.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(154, 62, '2010 - 2011', 'Xác Xuất Thống Kê 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2010 - 2011', 'exam', 'static/exams/JH3M9TDB_23052014902.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(155, 62, '2009 - 2010', 'Xác Xuất Thống Kê', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2009 - 2010', 'exam', 'static/exams/JH3M9TDB_23052014899.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(156, 11, '0', 'Đề Cương Văn Hóa Việt Nam Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Văn Hóa Việt Nam Đại Cương - 0', 'syllabus', 'static/exams/I6J714KA_xdocx.docx', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(157, 40, '2023-2024', 'Python 1', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Python - 2023-2024', 'exam', 'static/exams/89U4TI6J_v.pdf', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(158, 25, '2023 - 2024', 'Hướng Đối Tượng 2', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Hướng Đối Tượng - 2023 - 2024', 'exam', 'static/exams/PP3B0525_5142799a-7623-47e7-b5c6-b38ad2b3e17c.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(159, 57, '2023 - 2024', 'Phương Pháp Tính 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Pháp Tính - 2023 - 2024', 'exam', 'static/exams/NGITUGBR_70a9afa9-d805-4f1a-852c-047bb645daac.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(160, 55, '2023 - 2024', 'Giải Tích Hè', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2023 - 2024', 'exam', 'static/exams/F9V5F6ZU_3a8188a5-d531-454c-b503-de2cf5ba94c3.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(161, 61, '2014 - 2015', 'Toán Rời Rạc 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2014 - 2015', 'exam', 'static/exams/89U4TI6J_d7f4cb0a-ff23-4f55-930c-a23eae20e8e2.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(162, 61, '2016 - 2017', 'Toán Rời Rạc', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2016 - 2017', 'exam', 'static/exams/714KAE8M_bac1e0b7-11ea-47a3-9ac0-7236eafc5dfc.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(163, 61, '2011 - 2012', 'Toán Rời Rạc 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2011 - 2012', 'exam', 'static/exams/EP9NSMVW_e5db90d2-b07b-4d02-bcc4-5d506f9039da.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(164, 20, '2023 - 2024', 'Triết Học Mác', 'Trường Đại học Khoa học - Môn học đại cương - Môn Triết Học Mác - 2023 - 2024', 'exam', 'static/exams/833RVXRQ_z6151857411454_728be5f5920b9b156818d5a4130d688c.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(165, 6, '2023 - 2024', 'Môi Trường Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Môi Trường Đại Cương - 2023 - 2024', 'exam', 'static/exams/833RVXRQ_z6151857878799_262395caf813c71901344187a55350bf.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(166, 19, '2023 - 2024', 'Kinh Tế Chính Trị Mác 1', 'Trường Đại học Khoa học - Môn học đại cương - Môn Kinh Tế Chính Trị Mác - 2023 - 2024', 'exam', 'static/exams/833RVXRQ_z6151858756366_30ba132209b0ec33fc27ea3ab42fd230.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(167, 5, '2023 - 2024', 'Lịch Sử Việt Nam Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Lịch Sử Việt Nam Đại Cương - 2023 - 2024', 'exam', 'static/exams/833RVXRQ_z6151859385578_ac434bdd3b0ec35dae785c1abdd2beab.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(168, 103, '2022 - 2023', 'Xứ Lý Tín Hiệu Số 1', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Xử Lý Tín Hiệu Số 1 - 2022 - 2023', 'exam', 'static/exams/L6DSHJRS_IMG_2976.JPG', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(169, 102, '2019 - 2020', 'Xứ Lý Số Tín Hiệu', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Xử Lý Số Tín Hiệu - 2019 - 2020', 'exam', 'static/exams/3H96UIED_IMG_2976.JPG', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(170, 62, '2017 - 2018', 'Xác Xuất Thống Kê', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2017 - 2018', 'exam', 'static/exams/W3YL38TG_received_590087941689445.jpeg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(171, 62, '2018 - 2019', 'Xác Xuất Thống Kê 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2018 - 2019', 'exam', 'static/exams/L6DSHJRS_received_755670041874930.jpeg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(172, 62, '2019 - 2020', 'Xác Xuất Thống Kê', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2019 - 2020', 'exam', 'static/exams/L6DSHJRS_IMG20210118184722[1].jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(173, 62, '2022 - 2023', 'Xác Xuất Thống Kê 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2022 - 2023', 'exam', 'static/exams/GMAS6MOU_xttk22-23.png', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(174, 62, '2023 - 2024', 'Xác Xuất Thống Kê', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2023 - 2024', 'exam', 'static/exams/S8F7RIV1_xttk23-24.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(175, 106, '2022 - 2023', 'Vi Xử Lý Và Vi Điều Khiển Trong Đo Lường Tự Động', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Vi Xử Lý Và Vi Điều Khiển Trong Đo Lường Tự Động - 2022 - 2023', 'exam', 'static/exams/GMAS6MOU_2022-2023.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(176, 12, '2012 - 2013', 'Vật Lý Đại Cương 2', 'Trường Đại học Khoa học - Môn học đại cương - Môn Vật Lý Đại Cương - 2012 - 2013', 'exam', 'static/exams/3SS122PQ_2012-2013.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(177, 12, '2020 - 2021', 'Vật Lý Đại Cương 2', 'Trường Đại học Khoa học - Môn học đại cương - Môn Vật Lý Đại Cương - 2020 - 2021', 'exam', 'static/exams/G4CZ3NNI_2020-2021.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(178, 12, '2012 - 2013', 'Vật Lý Đại Cương 2 1', 'Trường Đại học Khoa học - Môn học đại cương - Môn Vật Lý Đại Cương - 2012 - 2013', 'exam', 'static/exams/2QZWLPYU_2012-2013c.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(179, 12, '2019 - 2020', 'Vật Lý Đại Cương 2', 'Trường Đại học Khoa học - Môn học đại cương - Môn Vật Lý Đại Cương - 2019 - 2020', 'exam', 'static/exams/78GYJ5UP_2019-2020.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(180, 12, '2022 - 2023', 'Vật Lý Đại Cương 2', 'Trường Đại học Khoa học - Môn học đại cương - Môn Vật Lý Đại Cương - 2022 - 2023', 'exam', 'static/exams/CKOP97SM_2022-2023x.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(181, 12, '2023 - 2024', 'Vật Lý Đại Cương 2', 'Trường Đại học Khoa học - Môn học đại cương - Môn Vật Lý Đại Cương - 2023 - 2024', 'exam', 'static/exams/3SS122PQ_vc.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(182, 18, '2019 - 2020', 'Tư Tưởng HCM', 'Trường Đại học Khoa học - Môn học đại cương - Môn Tư Tưởng HCM - 2019 - 2020', 'exam', 'static/exams/N2FHDFGF_Scanned_20210109-1502.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(183, 20, '2019 - 2020', 'Triết Học Mác', 'Trường Đại học Khoa học - Môn học đại cương - Môn Triết Học Mác - 2019 - 2020', 'exam', 'static/exams/Y33A3OB7_2019-2020v.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(184, 20, '2020 - 2021', 'Triết Học Mác', 'Trường Đại học Khoa học - Môn học đại cương - Môn Triết Học Mác - 2020 - 2021', 'exam', 'static/exams/1PH854H5_2020-2021xx.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(185, 20, '2020 - 2021', 'Triết Học Mác 1', 'Trường Đại học Khoa học - Môn học đại cương - Môn Triết Học Mác - 2020 - 2021', 'exam', 'static/exams/G4CZ3NNI_2020-202.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(186, 20, '2022 - 2023', 'Triết Học Mác 1', 'Trường Đại học Khoa học - Môn học đại cương - Môn Triết Học Mác - 2022 - 2023', 'exam', 'static/exams/2QZWLPYU_2022-2023cc.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(187, 20, '2023 - 2024', 'Triết Học Mác 1', 'Trường Đại học Khoa học - Môn học đại cương - Môn Triết Học Mác - 2023 - 2024', 'exam', 'static/exams/N2FHDFGF_v.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(188, 20, '0', 'Đề cương học phần Triết Học Mác', 'Trường Đại học Khoa học - Môn học đại cương - Môn Triết Học Mác - 0', 'syllabus', 'static/exams/1PH854H5_xv.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(189, 66, '2019 - 2020', 'Toán Chuyên Nghành', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Chuyên Nghành - 2019 - 2020', 'exam', 'static/exams/GOP6UE2J_zx.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(190, 66, '2020 - 2021', 'Toán Chuyên Nghành', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Chuyên Nghành - 2020 - 2021', 'exam', 'static/exams/INPH988U_136104805_2856657007994148_3896520501315031389_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(191, 66, '2023 - 2024', 'Toán Chuyên Nghành', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Chuyên Nghành - 2023 - 2024', 'exam', 'static/exams/M90FMTL9_tcn23-24.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(192, 100, '2022 - 2023', 'Thông Tin Số', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Thông Tin Số - 2022 - 2023', 'exam', 'static/exams/V9Q88NUR_IMG_2973.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(193, 0, '0', 'Đề cương học phần Thiết Bị Đầu Cuối Và Các Dịch Vụ Viễn Thông', '', 'syllabus', 'static/exams/AMRLLOSF_Cdocx.pdf', '2025-02-20 03:34:30', '2025-02-20 03:36:28'),
(194, 60, '2016 - 2017', 'Phương Trình Vi Phân', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Trình Vi Phân - 2016 - 2017', 'exam', 'static/exams/GOP6UE2J_2016-2017.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(195, 60, '2014 - 2015', 'Phương Trình Vi Phân', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Trình Vi Phân - 2014 - 2015', 'exam', 'static/exams/9GHIZ7HR_2014-2015.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(196, 60, '2019 - 2020', 'Phương Trình Vi Phân', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Trình Vi Phân - 2019 - 2020', 'exam', 'static/exams/V9Q88NUR_2019-20201.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(197, 60, '2019 - 2020', 'Phương Trình Vi Phân 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Trình Vi Phân - 2019 - 2020', 'exam', 'static/exams/17CGZN74_2019-2.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(198, 57, '2019 - 2020', 'Phương Pháp Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Phương Pháp Tính - 2019 - 2020', 'exam', 'static/exams/NP6X7ABX_Scanned_20210109-1430.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(199, 39, '2020 - 2021', 'Phân Tích Hệ Thống Thông Tin', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Phân Tích Hệ Thống Thông Tin - 2020 - 2021', 'exam', 'static/exams/LNE8A7E7_139767354_163824431856563_8087341802310785956_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(200, 98, '2019 - 2020', 'Nguồn Điện', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Nguồn Điện - 2019 - 2020', 'exam', 'static/exams/UX8M9326_Scanned_20210109-1429.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(201, 0, '0', 'Đề cương ôn tập học phần Mạng Viễn Thông', '', 'syllabus', 'static/exams/17CGZN74_on-tap-MANG-VIEN-THONG-2020.pdf', '2025-02-20 03:34:30', '2025-02-20 03:36:28'),
(202, 0, '0', 'Đề cương ôn tập học phần Mạng Ngoại Vi', '', 'syllabus', 'static/exams/9N2RHSWB_cx.pdf', '2025-02-20 03:34:30', '2025-02-20 03:36:28'),
(203, 96, '2019 - 2020', 'Lý Thuyết Trường Điện Từ', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Lý Thuyết Trường Điện Từ - 2019 - 2020', 'exam', 'static/exams/QNYI0K5W_117049093_1223960861295184_6480807839484786610_o.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(204, 96, '2020 - 2021', 'Lý Thuyết Trường Điện Từ', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Lý Thuyết Trường Điện Từ - 2020 - 2021', 'exam', 'static/exams/DHKVJR7D_IMG20210118180725.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(205, 96, '2023 - 2024', 'Lý Thuyết Trường Điện Từ', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Lý Thuyết Trường Điện Từ - 2023 - 2024', 'exam', 'static/exams/GQ2U39GQ_lttdt23-24.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(206, 95, '2020 - 2021', 'Lý Thuyết Truyền Sóng', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Lý Thuyết Truyền Sóng - 2020 - 2021', 'exam', 'static/exams/6TNU1JDS_137597935_395508044881104_6450873792475580544_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(207, 94, '2022 - 2023', 'Lý Thuyết Mạch', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Lý Thuyết Mạch - 2022 - 2023', 'exam', 'static/exams/9HNICMXS_2022-20.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(208, 94, '2022 - 2023', 'Lý Thuyết Mạch 1', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Lý Thuyết Mạch - 2022 - 2023', 'exam', 'static/exams/ZY4BPN8N_ccc.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(209, 94, '2020 - 2021', 'Lý Thuyết Mạch', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Lý Thuyết Mạch - 2020 - 2021', 'exam', 'static/exams/272UQN48_d2020-2021.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45');
INSERT INTO `documents` (`id`, `subject_id`, `year`, `file_name`, `file_info`, `document_type`, `file_path`, `created_at`, `updated_at`) VALUES
(210, 94, '2015 - 2016', 'Lý Thuyết Mạch', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Lý Thuyết Mạch - 2015 - 2016', 'exam', 'static/exams/QNYI0K5W_ccccc.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(211, 94, '2017 - 2018', 'Lý Thuyết Mạch', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Lý Thuyết Mạch - 2017 - 2018', 'exam', 'static/exams/Y951YWKD_c2017-2018.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(212, 94, '2018 - 2019', 'Lý Thuyết Mạch', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Lý Thuyết Mạch - 2018 - 2019', 'exam', 'static/exams/21JZMAL9_vv2018-2019.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(213, 94, '2019 - 2020', 'Lý Thuyết Mạch', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Lý Thuyết Mạch - 2019 - 2020', 'exam', 'static/exams/W3SWMEF8_ccc2019-2020.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(214, 97, '2015 - 2016', 'Lý Thuyết Điều Khiển Tự Động', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Lý Thuyết Điều Khiển Tự Động - 2015 - 2016', 'exam', 'static/exams/U2KZG7AW_IMG20210118180538.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(215, 97, '2016 - 2017', 'Lý Thuyết Điều Khiển Tự Động', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Lý Thuyết Điều Khiển Tự Động - 2016 - 2017', 'exam', 'static/exams/K32JIO7X_IMG20210118180547.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(216, 97, '2018 - 2019', 'Lý Thuyết Điều Khiển Tự Động', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Lý Thuyết Điều Khiển Tự Động - 2018 - 2019', 'exam', 'static/exams/58JAFQIN_IMG20210118180604.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(217, 97, '2022 - 2023', 'Lý Thuyết Điều Khiển Tự Động', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Lý Thuyết Điều Khiển Tự Động - 2022 - 2023', 'exam', 'static/exams/T8BL2J3Q_ltdktd2-23.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(218, 0, '2022 - 2023', 'Lịch Sử Đảng Việt Nam', '', 'exam', 'static/exams/FV6SJGPO_IMG_2791.JPG', '2025-02-20 03:34:30', '2025-02-20 05:04:26'),
(219, 93, '2015 - 2016', 'Kỹ Thuật Số', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Kỹ Thuật Số - 2015 - 2016', 'exam', 'static/exams/O7Y9PHVP_IMG20210118185024.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(220, 93, '2016 - 2017', 'Kỹ Thuật Số', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Kỹ Thuật Số - 2016 - 2017', 'exam', 'static/exams/FBB8B4XA_IMG20210118185010.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(221, 93, '2019 - 2020', 'Kỹ Thuật Số', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Kỹ Thuật Số - 2019 - 2020', 'exam', 'static/exams/L6DSHJRS_Scanned_20210109-1502x.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(222, 93, '2022 - 2023', 'Kỹ Thuật Số', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Kỹ Thuật Số - 2022 - 2023', 'exam', 'static/exams/S8F7RIV1_kts22-23.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(223, 92, '2016 - 2017', 'Kỹ Thuật Siêu Cao Tần', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Kỹ Thuật Siêu Cao Tần - 2016 - 2017', 'exam', 'static/exams/GMAS6MOU_Scanned_20210109-1712.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(224, 92, '2018 - 2019', 'Kỹ Thuật Siêu Cao Tần', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Kỹ Thuật Siêu Cao Tần - 2018 - 2019', 'exam', 'static/exams/970AXLEN_Scanned_20210109-1711.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(225, 92, '2019 - 2020', 'Kỹ Thuật Siêu Cao Tần', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Kỹ Thuật Siêu Cao Tần - 2019 - 2020', 'exam', 'static/exams/3SS122PQ_Scanned_20210109-1715.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(226, 92, '2022 - 2023', 'Kỹ Thuật Siêu Cao Tần', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Kỹ Thuật Siêu Cao Tần - 2022 - 2023', 'exam', 'static/exams/G4CZ3NNI_ktsct22-23.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(227, 92, '2023 - 2024', 'Kỹ Thuật Siêu Cao Tần', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Kỹ Thuật Siêu Cao Tần - 2023 - 2024', 'exam', 'static/exams/2QZWLPYU_z5499165985799_282ee02c9b14c98154431cdff46a137e.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(228, 91, '2019 - 2020', 'Kỹ Thuật Mạch Điện Tử', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Kỹ Thuật Mạch Điện Tử - 2019 - 2020', 'exam', 'static/exams/N2FHDFGF_Scanned_20210109-14c29.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(229, 91, '2022 - 2023', 'Kỹ Thuật Mạch Điện Tử', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Kỹ Thuật Mạch Điện Tử - 2022 - 2023', 'exam', 'static/exams/1PH854H5_ktmdt22-23.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(230, 19, '2020 - 2021', 'Kinh Tế Chính Trị Mác', 'Trường Đại học Khoa học - Môn học đại cương - Môn Kinh Tế Chính Trị Mác - 2020 - 2021', 'exam', 'static/exams/GOP6UE2J_IMG_20210118_180306.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(231, 19, '2023 - 2024', 'Kinh Tế Chính Trị Mác 2', 'Trường Đại học Khoa học - Môn học đại cương - Môn Kinh Tế Chính Trị Mác - 2023 - 2024', 'exam', 'static/exams/L6DSHJRS_ktct3-24.png', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(232, 101, '2020 - 2021', 'Vi Xử Lí', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Vi Xử Lí - 2020 - 2021', 'exam', 'static/exams/58HA1BCY_IMG20210118180738.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(233, 101, '2023 - 2024', 'Vi Xử Lí', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Vi Xử Lí - 2023 - 2024', 'exam', 'static/exams/NGKS92A5_KTVXL-23-24.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(234, 6, '2022 - 2023', 'Môi Trường Đại Cương 1', 'Trường Đại học Khoa học - Môn học đại cương - Môn Môi Trường Đại Cương - 2022 - 2023', 'exam', 'static/exams/7WA9FOJ8_gdmt22-23.png', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(235, 105, '2023 - 2024', 'Đo Lường Điện Tử Viễn Thông', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Đo Lường Điện Tử Viễn Thông - 2023 - 2024', 'exam', 'static/exams/V9Q88NUR_dldtvt23-24.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(236, 104, '2020 - 2021', 'Điện Tử Ứng Dụng', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Điện Tử Ứng Dụng - 2020 - 2021', 'exam', 'static/exams/RYF4SCV9_IMG20210118180753.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(237, 55, '2019 - 2020', 'Đại Số Tuyến Tính Và Hình Học Giải Tích', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2019 - 2020', 'exam', 'static/exams/BSE84V6E_2019-202.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(238, 55, '2020 - 2021', 'Đại Số Tuyến Tính Và Hình Học Giải Tích', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2020 - 2021', 'exam', 'static/exams/DK7F92NJ_2020-2021c.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(239, 63, '2022 - 2023', 'Đại Số Tuyến Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Đại Số Tuyến Tính - 2022 - 2023', 'exam', 'static/exams/17CGZN74_dstt22-23.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(240, 63, '2023 - 2024', 'Đại Số Tuyến Tính 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Đại Số Tuyến Tính - 2023 - 2024', 'exam', 'static/exams/S8F7RIV1_ccz.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(241, 88, '2020 - 2021', 'Cơ Sở Lí Thuyết Thông Tin', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Cơ Sở Lí Thuyết Thông Tin - 2020 - 2021', 'exam', 'static/exams/GMAS6MOU_20210109_091747.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(242, 88, '2022 - 2023', 'Cơ Sở Lí Thuyết Thông Tin', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Cơ Sở Lí Thuyết Thông Tin - 2022 - 2023', 'exam', 'static/exams/3SS122PQ_cslttt22-23.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(243, 88, '2023 - 2024', 'Cơ Sở Lí Thuyết Thông Tin', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Cơ Sở Lí Thuyết Thông Tin - 2023 - 2024', 'exam', 'static/exams/G4CZ3NNI_cslttt23-24.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(244, 16, '2022 - 2023', 'Chủ Nghĩa Xã Hội Khoa Học', 'Trường Đại học Khoa học - Môn học đại cương - Môn Chủ Nghĩa Xã Hội Khoa Học - 2022 - 2023', 'exam', 'static/exams/LNE8A7E7_cnxhh22-23.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(245, 87, '2020 - 2021', 'Cơ Sở Kỹ Thuật Truyền Số Liệu', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Cơ Sở Kỹ Thuật Truyền Số Liệu - 2020 - 2021', 'exam', 'static/exams/9HNICMXS_139285308_791154021491083_1846145977283977045_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(246, 87, '2022 - 2023', 'Cơ Sở Kỹ Thuật Truyền Số Liệu', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Cơ Sở Kỹ Thuật Truyền Số Liệu - 2022 - 2023', 'exam', 'static/exams/2QZWLPYU_cskttsl122-23.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(247, 86, '2020 - 2021', 'Cơ Sở Kỹ Thuật Chuyển Mạch', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Cơ Sở Kỹ Thuật Chuyển Mạch - 2020 - 2021', 'exam', 'static/exams/N2FHDFGF_139205510_484453402721222_6790890495940339842_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(248, 86, '2022 - 2023', 'Cơ Sở Kỹ Thuật Chuyển Mạch', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Cơ Sở Kỹ Thuật Chuyển Mạch - 2022 - 2023', 'exam', 'static/exams/272UQN48_IMG_2792.JPG', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(249, 90, '2022 - 2023', 'Cấu Kiện Điện Tử - Quang Điện Tử', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Cấu Kiện Điện Tử - Quang Điện Tử - 2022 - 2023', 'exam', 'static/exams/9N2RHSWB_1.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(250, 85, '2023 - 2024', 'Anh Văn Chuyên Ngành', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Anh Văn Chuyên Ngành - 2023 - 2024', 'exam', 'static/exams/1PH854H5_avcn13-24.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(251, 25, '2021-2022', 'Hướng Đối Tượng 1', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Hướng Đối Tượng - 2021-2022', 'exam', 'static/exams/T8J24TH1_Screenshot_20241101-113905_OneDrive.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(252, 35, '2014 - 2015', 'Nguyên Lí Hệ Điều Hành', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nguyên Lí Hệ Điều Hành - 2014 - 2015', 'exam', 'static/exams/KHKRYY5J_cdc03323-2726-402f-81c0-76930aac044a.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(253, 35, '2012 - 2013', 'Nguyên Lí Hệ Điều Hành', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nguyên Lí Hệ Điều Hành - 2012 - 2013', 'exam', 'static/exams/JD5NY0BO_51f52463-b083-4d0c-9a06-53fd2d8e1487.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(254, 40, '2021 - 2022', 'Python', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Python - 2021 - 2022', 'exam', 'static/exams/KHKRYY5J_063d55ba-fe2f-4cb6-86e7-6c6680561d4e.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(255, 24, '2022 - 2023', 'Font End', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Font End - 2022 - 2023', 'exam', 'static/exams/ETPEYWIU_438246216_418487684308774_8042750199502997115_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(256, 40, '2023 - 2024', 'Python', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Python - 2023 - 2024', 'exam', 'static/exams/ETPEYWIU_56aa6048-c465-4034-b420-54266b32d977.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(257, 61, '2015 - 2016', 'Toán Rời Rạc Kỳ Hè', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2015 - 2016', 'exam', 'static/exams/ETPEYWIU_367080e2-0767-403f-b857-19e160626b13.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(258, 61, '2022 - 2023', 'Toán Rời Rạc', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2022 - 2023', 'exam', 'static/exams/1EZYV8CZ_aeb4da0a-1b14-4810-b342-cc3a247d073f.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(259, 35, '2022 - 2023', 'Nguyên Lí Hệ Điều Hành', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nguyên Lí Hệ Điều Hành - 2022 - 2023', 'exam', 'static/exams/T6C7ZNPQ_f10d5ec7-605e-4db3-bb5f-3b74807571a0.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(260, 58, '2022 - 2023', 'Phép Tính Tích Phân Và Hàm Một Biến', 'Trường Đại học Khoa học - Khoa Toán - Môn Phép Tính Tích Phân Và Hàm Một Biến - 2022 - 2023', 'exam', 'static/exams/ETPEYWIU_Screenshot 2024-12-23 235657.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(261, 58, '2022 - 2023', 'Phép Tính Tích Phân Và Hàm Một Biến 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Phép Tính Tích Phân Và Hàm Một Biến - 2022 - 2023', 'exam', 'static/exams/1EZYV8CZ_Screenshot 2024-12-23 235801.png', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(262, 58, '2022 - 2023', 'Phép Tính Tích Phân Và Hàm Một Biến 2', 'Trường Đại học Khoa học - Khoa Toán - Môn Phép Tính Tích Phân Và Hàm Một Biến - 2022 - 2023', 'exam', 'static/exams/T6C7ZNPQ_Screenshot 2024-12-24 000004.png', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(263, 58, '2022 - 2023', 'Phép Tính Tích Phân Và Hàm Một Biến 3', 'Trường Đại học Khoa học - Khoa Toán - Môn Phép Tính Tích Phân Và Hàm Một Biến - 2022 - 2023', 'exam', 'static/exams/ETPEYWIU_Screenshot 2024-12-24 000033.png', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(264, 58, '2022 - 2023', 'Phép Tính Tích Phân Và Hàm Một Biến 4', 'Trường Đại học Khoa học - Khoa Toán - Môn Phép Tính Tích Phân Và Hàm Một Biến - 2022 - 2023', 'exam', 'static/exams/1EZYV8CZ_Screenshot 2024-12-24 000102.png', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(265, 58, '2022 - 2023', 'Phép Tính Tích Phân Và Hàm Một Biến 5', 'Trường Đại học Khoa học - Khoa Toán - Môn Phép Tính Tích Phân Và Hàm Một Biến - 2022 - 2023', 'exam', 'static/exams/T6C7ZNPQ_Screenshot 2024-12-24 000127.png', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(266, 58, '2022 - 2023', 'Phép Tính Tích Phân Và Hàm Một Biến 6', 'Trường Đại học Khoa học - Khoa Toán - Môn Phép Tính Tích Phân Và Hàm Một Biến - 2022 - 2023', 'exam', 'static/exams/ZRAA0EHM_Screenshot 2024-12-24 000153.png', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(267, 58, '2022 - 2023', 'Phép Tính Tích Phân Và Hàm Một Biến 7', 'Trường Đại học Khoa học - Khoa Toán - Môn Phép Tính Tích Phân Và Hàm Một Biến - 2022 - 2023', 'exam', 'static/exams/2BN6HFOV_Screenshot 2024-12-24 000220.png', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(268, 58, '2022 - 2023', 'Phép Tính Tích Phân Và Hàm Một Biến 8', 'Trường Đại học Khoa học - Khoa Toán - Môn Phép Tính Tích Phân Và Hàm Một Biến - 2022 - 2023', 'exam', 'static/exams/5NCIOOGA_Screenshot 2024-12-24 000244.png', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(269, 58, '2022 - 2023', 'Phép Tính Tích Phân Và Hàm Một Biến 9', 'Trường Đại học Khoa học - Khoa Toán - Môn Phép Tính Tích Phân Và Hàm Một Biến - 2022 - 2023', 'exam', 'static/exams/23DMGPP4_Screenshot2024-12-24000309.png', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(270, 6, '0', 'Đề cương học phần Môi Trường Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Môi Trường Đại Cương - 0', 'syllabus', 'static/exams/1EZYV8CZ_vvv.docx', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(271, 11, '0', 'Ngân hàng đề thi học phần Văn Hóa Việt Nam Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Văn Hóa Việt Nam Đại Cương - 0', 'syllabus', 'static/exams/ETPEYWIU_v.docx', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(272, 21, '2023 - 2024', 'Tâm Lý Học Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Tâm Lý Học Đại Cương - 2023 - 2024', 'exam', 'static/exams/T048YNAM_462587341_615577241127896_8394522352465514999_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(273, 157, '2023 - 2024', 'Phương Pháp Luận Nghiên Cứu Khoa Học', 'Trường Đại học Khoa học - Khoa Xã hội học và Công tác xã hội - Môn Phương Pháp Luận Nghiên Cứu Khoa Học - 2023 - 2024', 'exam', 'static/exams/T048YNAM_470052783_1259234215361841_8733791616382205700_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(274, 37, '2023 - 2024', 'Nhập Môn Lập Trình', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nhập Môn Lập Trình - 2023 - 2024', 'exam', 'static/exams/T048YNAM_IMG_20241217_200908.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(275, 31, '2022 - 2023', 'Lập Trình Nâng Cao', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Lập Trình Nâng Cao - 2022 - 2023', 'exam', 'static/exams/UHGPCKB0_De01.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(276, 62, '2023 - 2024', 'Xác Xuất Thống Kê 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2023 - 2024', 'exam', 'static/exams/J5IYH1N7_20e09580-7eb1-47c6-bfd0-2bd5897051b3.pdf', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(277, 62, '2023 - 2024', 'Xác Xuất Thống Kê 2', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2023 - 2024', 'exam', 'static/exams/OIOUZL7P_7f800014-8a25-409b-bd8a-5d3e724bccd5.pdf', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(278, 63, '2013 - 2014', 'Đại Số Tuyến Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Đại Số Tuyến Tính - 2013 - 2014', 'exam', 'static/exams/3NA4JFVI_c53c017b-c1e5-49d2-be42-82ea727f95df.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(279, 55, '2008 - 2009', 'Đại Số Tuyến Tính Và Hình Học Giải Tích', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2008 - 2009', 'exam', 'static/exams/OIOUZL7P_c38265fa-92b8-43ef-8515-5b96e1cc9b25.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(280, 63, '2013 - 2014', 'Đại Số Tuyến Tính 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Đại Số Tuyến Tính - 2013 - 2014', 'exam', 'static/exams/O7AYELD1_9a8a8abe-4321-4b5b-a2d3-3123654070a0.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(281, 55, '2013 - 2014', 'Đại Số Tuyến Tính Và Hình Học Giải Tích', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2013 - 2014', 'exam', 'static/exams/O7AYELD1_07ccc032-05e1-4007-939e-aec09c6383d0.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(282, 55, '2013 - 2014', 'Đại Số Tuyến Tính Và Hình Học Giải Tích 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2013 - 2014', 'exam', 'static/exams/H5680O84_c8e0fc51-af0a-4cc0-9b09-3eff0e052955.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(283, 63, '2012 - 2013', 'Đại Số Tuyến Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Đại Số Tuyến Tính - 2012 - 2013', 'exam', 'static/exams/9WN5AK8P_66de6bde-af48-477d-b59c-90ac9b28479b.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(284, 55, '2013 - 2014', 'Đại Số Tuyến Tính Và Hình Học Giải Tích 2', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2013 - 2014', 'exam', 'static/exams/Y0CHVWN8_fca188ad-03db-4654-b4f9-5be0e6d81c99.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(285, 63, '2015 - 2016', 'Đại Số Tuyến Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Đại Số Tuyến Tính - 2015 - 2016', 'exam', 'static/exams/Y0CHVWN8_282d5623-77fa-4e5a-9b6a-3fa2086b54b1.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(286, 55, '2012 - 2013', 'Đại Số Tuyến Tính Và Hình Học Giải Tích', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2012 - 2013', 'exam', 'static/exams/Y0CHVWN8_53e33b30-ac2f-4f5a-be07-24778028e692.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(287, 55, '2014 - 2015', 'Đại Số Tuyến Tính Và Hình Học Giải Tích', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2014 - 2015', 'exam', 'static/exams/HJ7A152S_49784cd9-1155-4561-abc6-d38f390935f8.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(288, 55, '2012 - 2013', 'Đại Số Tuyến Tính Và Hình Học Giải Tích 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2012 - 2013', 'exam', 'static/exams/HJ7A152S_d0c71e20-393f-4c07-9612-a450bf14c68c.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(289, 63, '2015 - 2016', 'Đại Số Tuyến Tính Kỳ Hè', 'Trường Đại học Khoa học - Khoa Toán - Môn Đại Số Tuyến Tính - 2015 - 2016', 'exam', 'static/exams/MIT3B2MD_09d21fca-fa4f-4b1e-9d0e-716261d7c6c4.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(290, 45, '2022 - 2023', 'SQL', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn SQL - 2022 - 2023', 'exam', 'static/exams/LD2OJMD4_e690654c-c1c4-4dc8-a0c5-f987c8843baa.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(291, 9, '2022 - 2023', 'Pháp Luật Việt Nam Đại Cương 2', 'Trường Đại học Khoa học - Môn học đại cương - Môn Pháp Luật Việt Nam Đại Cương - 0', 'exam', 'static/exams/JYMD52TK_266d491d-2eeb-446d-a59f-86672c2d2808.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(292, 27, '2022 - 2023', 'Java Nâng Cao', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Java Nâng Cao - 0', 'exam', 'static/exams/LD2OJMD4_c05922fb-3b29-4f90-b84d-4a705cd3f697.jpg', '2025-02-20 03:34:30', '2025-02-20 11:01:34'),
(293, 25, '2023 - 2024', 'Hướng Đối Tượng 3', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Hướng Đối Tượng - 2023 - 2024', 'exam', 'static/exams/IXWOTNUP_6799a2de-82f3-49e4-a267-6b80e0cd1737.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(294, 36, '2023 - 2024', 'Nhập Môn Cơ Sở Dữ Liệu', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nhập Môn Cơ Sở Dữ Liệu - 2023 - 2024', 'exam', 'static/exams/C1AH53TF_470054099_1815663562589481_332444483969044693_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(295, 37, '2022 - 2023', 'Nhập Môn Lập Trình', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nhập Môn Lập Trình - 2022 - 2023', 'exam', 'static/exams/XXLF1I85_nbm.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(296, 37, '2023 - 2024', 'Nhập Môn Lập Trình 1', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nhập Môn Lập Trình - 2023 - 2024', 'exam', 'static/exams/6W1WJLIW_vvv.pdf', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(297, 54, '2023 - 2024', 'Cơ Sở Toán', 'Trường Đại học Khoa học - Khoa Toán - Môn Cơ Sở Toán - 2023 - 2024', 'exam', 'static/exams/EC36J8N0_2-7g30-29_12_2023.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(298, 36, '2011 - 2012', 'Nhập Môn Cơ Sở Dữ Liệu', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nhập Môn Cơ Sở Dữ Liệu - 2011 - 2012', 'exam', 'static/exams/ZACQK2BS_De-so-1-new.doc', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(299, 36, '2010 - 2011', 'Nhập Môn Cơ Sở Dữ Liệu', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nhập Môn Cơ Sở Dữ Liệu - 2010 - 2011', 'exam', 'static/exams/IAUADXAD_De-so-3-new.doc', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(300, 10, '2024 - 2025', 'Tôn Giáo Học Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Tôn Giáo Học Đại Cương - 2024 - 2025', 'exam', 'static/exams/HAZPU33K_e0fe15af-a857-4e60-9f89-a7f8a32f5467.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(301, 19, '2024 - 2025', 'Kinh Tế Chính Trị Mác', 'Trường Đại học Khoa học - Môn học đại cương - Môn Kinh Tế Chính Trị Mác - 2024 - 2025', 'exam', 'static/exams/V13HQS3A_z6180965516307_9248efbda7f74360a424db5024407aa1.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(302, 11, '2024 - 2025', 'Văn Hóa Việt Nam Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Văn Hóa Việt Nam Đại Cương - 2024 - 2025', 'exam', 'static/exams/HAZPU33K_466622304_581289614539023_3078587430793772245_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(303, 18, '2024 - 2025', 'Tư Tưởng HCM', 'Trường Đại học Khoa học - Môn học đại cương - Môn Tư Tưởng HCM - 2024 - 2025', 'exam', 'static/exams/V13HQS3A_7255941f-3202-448c-9e78-d950dc955f2b.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(304, 119, '2024 - 2025', 'Quản Lý Tài Nguyên Khoáng Sản Và Năng Lượng', 'Trường Đại học Khoa học - Khoa Địa lý - Địa chất - Môn Quản Lý Tài Nguyên Khoáng Sản Và Năng Lượng - 2024 - 2025', 'exam', 'static/exams/3CC46TAW_z6184260294268_37b3317094f929a82e3b03575d20f289.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(305, 131, '2024 - 2025', 'Hành Vi Con Người Và Xã Hội', 'Trường Đại học Khoa học - Khoa Xã hội học và Công tác xã hội - Môn Hành Vi Con Người Và Xã Hội - 2024 - 2025', 'exam', 'static/exams/3CC46TAW_z6184262927692_e870f3ab52c594559c2d3a507cb2179f.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(306, 51, '2024 - 2025', 'Truyền Thông Marketing Tích Hợp', 'Trường Đại học Khoa học - Khoa Báo chí - Truyền thông - Môn Truyền Thông Marketing Tích Hợp - 2024 - 2025', 'exam', 'static/exams/8I70R1YN_z6184262925528_6c8443b0d5473e97f51a37b1ba23ca4f.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(307, 115, '2024 - 2025', 'Hóa Học Phân Tích', 'Trường Đại học Khoa học - Khoa Hóa học - Môn Hóa Học Phân Tích - 2024 - 2025', 'exam', 'static/exams/5X5YCB8M_z6184262924228_9495b2715ce58985ba8437aa252fb3ce.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(308, 136, '2024 - 2025', 'Cơ Sở Khoa Học Của Con Đường Đi Lên Xã Hội Chủ Nghĩa Ở Việt Nam', 'Trường Đại học Khoa học - Khoa Lý luận chính trị - Môn Cơ Sở Khoa Học Của Con Đường Đi Lên Xã Hội Chủ Nghĩa Ở Việt Nam - 2024 - 2025', 'exam', 'static/exams/CI2XJYD2_z6184262722317_48dafc77bf3694c3e206f7695ab4dac0.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(309, 3, '2024 - 2025', 'Hóa Học Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Hóa Học Đại Cương - 2024 - 2025', 'exam', 'static/exams/8I70R1YN_967d2556-012f-4b9a-b74a-17334394f3e2.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(310, 42, '2024 - 2025', 'Thiết Kế Đồ Hoạ Ứng Dụng', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Thiết Kế Đồ Hoạ Ứng Dụng - 2024 - 2025', 'exam', 'static/exams/5X5YCB8M_z6184262904865_88db8fea88a80a7cbf4750907acd9130.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(311, 108, '2024 - 2025', 'Hình Học Họa Hình 1', 'Trường Đại học Khoa học - Khoa Kiến trúc - Môn Hình Học Họa Hình 1 - 2024 - 2025', 'exam', 'static/exams/HAZPU33K_z6184260351046_66ceeb19c592b85f124182ad18c721de.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(312, 35, '2024 - 2025', 'Nguyên Lí Hệ Điều Hành', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nguyên Lí Hệ Điều Hành - 2024 - 2025', 'exam', 'static/exams/V13HQS3A_z6184262810561_288e20a59454768666f25ac2c000460c.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(313, 137, '2024 - 2025', 'Giới Thiệu Các Tác Phẩm Tiêu Biểu Của HCM', 'Trường Đại học Khoa học - Khoa Lý luận chính trị - Môn Giới Thiệu Các Tác Phẩm Tiêu Biểu Của HCM - 2024 - 2025', 'exam', 'static/exams/HAZPU33K_z6184550116264_cc0f8a6d22f5aae3fd574cf6518777ae.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(314, 34, '0', 'Đề cương ôn tập Mạng Máy Tính', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Mạng Máy Tính - 0', 'syllabus', 'static/exams/HAZPU33K_vccc.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(315, 62, '2024 - 2025', 'Xác Xuất Thống Kê', 'Trường Đại học Khoa học - Khoa Toán - Môn Xác Xuất Thống Kê - 2024 - 2025', 'exam', 'static/exams/HAZPU33K_78ee8690-722d-4f97-aea0-4bfb50faeae2.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(316, 37, '2024 - 2025', 'Nhập Môn Lập Trình', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nhập Môn Lập Trình - 2024 - 2025', 'exam', 'static/exams/Y98IBEPL_denmlt2-1.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(317, 48, '2024 - 2025', 'Lịch Sử Báo Chí Việt Nam', 'Trường Đại học Khoa học - Khoa Báo chí - Truyền thông - Môn Lịch Sử Báo Chí Việt Nam - 2024 - 2025', 'exam', 'static/exams/66XTELEA_00950451-bfac-442d-b615-f4811f4f1d2a.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(318, 50, '2024 - 2025', 'Sáng Tạo Nội Dung Truyền Thông', 'Trường Đại học Khoa học - Khoa Báo chí - Truyền thông - Môn Sáng Tạo Nội Dung Truyền Thông - 2024 - 2025', 'exam', 'static/exams/9KZ9140H_26db0b92-1cb4-4f9d-9798-1eae20dc342e.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(319, 42, '2024 - 2025', 'Thiết Kế Đồ Hoạ Ứng Dụng 1', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Thiết Kế Đồ Hoạ Ứng Dụng - 2024 - 2025', 'exam', 'static/exams/AAI2YVO1_d4a5b21b-2ac4-4645-aead-891b37da393a.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(320, 24, '2024 - 2025', 'Font End', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Font End - 2024 - 2025', 'exam', 'static/exams/CW8OZNZF_image.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(321, 146, '2024 - 2025', 'Lịch Sử Tư Tưởng Phương Đông Và Việt Nam', 'Trường Đại học Khoa học - Khoa Lý luận chính trị - Môn Lịch Sử Tư Tưởng Phương Đông Và Việt Nam - 2024 - 2025', 'exam', 'static/exams/5RRMG7RQ_4c079aa5-973a-4470-b22b-3f61f307a913.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(322, 55, '2024 - 2025', 'Giải Tích Nâng Cao', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2024 - 2025', 'exam', 'static/exams/CW8OZNZF_111ff313-56d6-4d04-838c-91b9e3135499.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(323, 34, '2024 - 2025', 'Mạng Máy Tính', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Mạng Máy Tính - 2024 - 2025', 'exam', 'static/exams/CW8OZNZF_Mang_may_tinh_2024-2025.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(324, 26, '2023 - 2024', 'Java Cơ Bản', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Java Cơ Bản - 2023 - 2024', 'exam', 'static/exams/CW8OZNZF_3.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(325, 47, '2024 - 2025', 'Các Phương Tiện Truyền Thông Mới', 'Trường Đại học Khoa học - Khoa Báo chí - Truyền thông - Môn Các Phương Tiện Truyền Thông Mới - 2024 - 2025', 'exam', 'static/exams/JAS40KVL_z6193490607839_ca8a393f919875463c464693fefe7d4b.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(326, 46, '2024 - 2025', 'Báo In', 'Trường Đại học Khoa học - Khoa Báo chí - Truyền thông - Môn Báo In - 2024 - 2025', 'exam', 'static/exams/Y15W3IFB_z6193490570577_f37f903e7488db67c974c95fb2e1652a.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(327, 130, '2024 - 2025', 'Hành Vi Lệch Chuẩn Và Các Vấn Đề Lứa Tuổi', 'Trường Đại học Khoa học - Khoa Xã hội học và Công tác xã hội - Môn Hành Vi Lệch Chuẩn Và Các Vấn Đề Lứa Tuổi - 2024 - 2025', 'exam', 'static/exams/Y15W3IFB_z6193490771866_c8b1bb680315803d458b5a1bf9d02265.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(328, 117, '2024 - 2025', 'Quản Lý Môi Trường Doanh Nghiệp', 'Trường Đại học Khoa học - Khoa Môi trường - Môn Quản Lý Môi Trường Doanh Nghiệp - 2024 - 2025', 'exam', 'static/exams/IVID7LN3_z6193490708611_a50e57e68e9b0049125229396b4c8fc2.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(329, 116, '2024 - 2025', 'Công Nghệ Môi Trường', 'Trường Đại học Khoa học - Khoa Môi trường - Môn Công Nghệ Môi Trường - 2024 - 2025', 'exam', 'static/exams/SAPM5PTB_z6193490787741_bb54d2a8414e8a45176125fe24d0bc32.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(330, 127, '2024 - 2025', 'Địa Chất Việt Nam', 'Trường Đại học Khoa học - Khoa Địa lý - Địa chất - Môn Địa Chất Việt Nam - 2024 - 2025', 'exam', 'static/exams/IHZUS25A_z6193490750752_cd5efabb2417df69d3febf442b990902.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(331, 5, '2024 - 2025', 'Lịch Sử Việt Nam Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Lịch Sử Việt Nam Đại Cương - 2024 - 2025', 'exam', 'static/exams/Y15W3IFB_4c93eefe-8360-4500-91c6-8fcfce61bccd.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(333, 16, '2024 - 2025', 'Chủ Nghĩa Xã Hội Khoa Học', 'Trường Đại học Khoa học - Môn học đại cương - Môn Chủ Nghĩa Xã Hội Khoa Học - 2024 - 2025', 'exam', 'static/exams/Y15W3IFB_470051904_1540679809964143_7818023738695490804_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(334, 20, '2024 - 2025', 'Triết học Mác - Lênin', 'Trường Đại học Khoa học - Môn học đại cương - Môn Triết Học Mác - 2024 - 2025', 'exam', 'static/exams/NP4BVMU3_1000005904.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(335, 107, '2024 - 2025', 'Công Nghệ Chuyển Đổi Số Trong Kiến Trúc', 'Trường Đại học Khoa học - Khoa Kiến trúc - Môn Công Nghệ Chuyển Đổi Số Trong Kiến Trúc - 2024 - 2025', 'exam', 'static/exams/NP4BVMU3_a023a006-130f-4ea7-99e6-23e0420a6b94.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(336, 126, '2024 - 2025', 'Đánh Giá Tác Động Môi Trường Và Môi Trường Chiến Lược', 'Trường Đại học Khoa học - Khoa Địa lý - Địa chất - Môn Đánh Giá Tác Động Môi Trường Và Môi Trường Chiến Lược - 2024 - 2025', 'exam', 'static/exams/O5V1JNP4_cf8d3c80-a7b5-4340-8a4f-0bad60d87754.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(337, 124, '2024 - 2025', 'Quản Lý Tài Nguyên Và Môi Trường Đất', 'Trường Đại học Khoa học - Khoa Địa lý - Địa chất - Môn Quản Lý Tài Nguyên Và Môi Trường Đất - 2024 - 2025', 'exam', 'static/exams/BVMU3RY8_868851af-c922-4d21-96cd-f9ef3037bb4c.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(338, 20, '2024 - 2025', 'Triết học Mác - Lênin 1', 'Trường Đại học Khoa học - Môn học đại cương - Môn Triết Học Mác - 2024 - 2025', 'exam', 'static/exams/O5V1JNP4_inbound8845593479365700169.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(339, 72, '2024 - 2025', 'Nhập Môn Lí Luận Văn Học', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Nhập Môn Lí Luận Văn Học - 2024 - 2025', 'exam', 'static/exams/NUES5KAB_549fabb3-bb8e-4739-af7a-a8569a2ab199.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(340, 99, '2024 - 2025', 'Nghiên Cứu Và Xử Lí Thông Tin Định Lượng', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Nghiên Cứu Và Xử Lí Thông Tin Định Lượng - 2024 - 2025', 'exam', 'static/exams/10VOT93T_471661616_1385660932842810_507492360015412067_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(341, 73, '2023 - 2024', 'Tiến Trình Văn Học', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Tiến Trình Văn Học - 2023 - 2024', 'exam', 'static/exams/U543O7Z6_471720392_1773436393492560_8302406350699464175_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(342, 53, '2024 - 2025', 'Xã Hội Học Báo Chí', 'Trường Đại học Khoa học - Khoa Báo chí - Truyền thông - Môn Xã Hội Học Báo Chí - 2024 - 2025', 'exam', 'static/exams/5UCI3GIP_7794946c-c533-4f78-9792-08e3dcefc007.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(343, 145, '2024 - 2025', 'Lịch Sử Tư Tưởng Chính Trị Và Quản Lí', 'Trường Đại học Khoa học - Khoa Lý luận chính trị - Môn Lịch Sử Tư Tưởng Chính Trị Và Quản Lí - 2024 - 2025', 'exam', 'static/exams/W3607O14_z6201550971843_b79f328eabba1e89e47fa75643de42fc.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(344, 152, '2024 - 2025', 'Nhập Môn Khu Vực Học', 'Trường Đại học Khoa học - Khoa Lịch sử - Môn Nhập Môn Khu Vực Học - 2024 - 2025', 'exam', 'static/exams/4K3LKTF8_b8421d5e-811a-4f8c-bfdf-1dc7e19c28d6.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(345, 82, '2024 - 2025', 'Văn Học Dân Gian', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Văn Học Dân Gian - 2024 - 2025', 'exam', 'static/exams/W3607O14_ef04b431-e47c-460b-bb17-c1abe54d9c52.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(346, 9, '2024 - 2025', 'Pháp Luật Việt Nam Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Pháp Luật Việt Nam Đại Cương - 2024 - 2025', 'exam', 'static/exams/W3607O14_d01afecb-6569-458b-93d9-8c3d80e7ebdc.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(347, 132, '2024 - 2025', 'Nhập Môn Công Tác Xã Hội', 'Trường Đại học Khoa học - Khoa Xã hội học và Công tác xã hội - Môn Nhập Môn Công Tác Xã Hội - 2024 - 2025', 'exam', 'static/exams/K3LKTF8U_737a386c-89de-417d-bd4a-2c43b80f3a9b.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(348, 147, '2024 - 2025', 'Lịch Sử Việt Nam Cổ Đại Từ Nguyên Thủy Đến 1407', 'Trường Đại học Khoa học - Khoa Lịch sử - Môn Lịch Sử Việt Nam Cổ Đại Từ Nguyên Thủy Đến 1407 - 2024 - 2025', 'exam', 'static/exams/W3607O14_32cf2d91-c658-4c22-aeb1-4bd99ffe7d2b.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(349, 146, '2024 - 2025', 'Lịch Sử Tư Tưởng Phương Đông Và Việt Nam 1', 'Trường Đại học Khoa học - Khoa Lý luận chính trị - Môn Lịch Sử Tư Tưởng Phương Đông Và Việt Nam - 2024 - 2025', 'exam', 'static/exams/W3607O14_fb41b10d-f9be-4803-b800-caf3735e9e2f.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(350, 108, '2024 - 2025', 'Hình Học Họa Hình 1 1', 'Trường Đại học Khoa học - Khoa Kiến trúc - Môn Hình Học Họa Hình 1 - 2024 - 2025', 'exam', 'static/exams/W3607O14_472570654_519749091120747_8358105093888996192_n.pdf', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(351, 134, '2024 - 2025', 'Các Vấn Đề Xã Hội Đương Đại', 'Trường Đại học Khoa học - Khoa Xã hội học và Công tác xã hội - Môn Các Vấn Đề Xã Hội Đương Đại - 2024 - 2025', 'exam', 'static/exams/W3607O14_466758147_568229052700871_4778753225056821757_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(352, 63, '2024 - 2025', 'Đại Số Tuyến Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Đại Số Tuyến Tính - 2024 - 2025', 'exam', 'static/exams/1Z72E7QP_dst.png', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(353, 112, '2024 - 2025', 'Quy Hoạch Xây Dựng Và Phát Triển Đô Thị', 'Trường Đại học Khoa học - Khoa Kiến trúc - Môn Quy Hoạch Xây Dựng Và Phát Triển Đô Thị - 2024 - 2025', 'exam', 'static/exams/EY36TTKT_z6205695435256_3f7de722337992c41da27ca0d61676cc.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(354, 110, '2024 - 2025', 'Kỹ Thuật Xây Dựng Văn Bản', 'Trường Đại học Khoa học - Khoa Kiến trúc - Môn Kỹ Thuật Xây Dựng Văn Bản - 2024 - 2025', 'exam', 'static/exams/YT360VTH_z6205695617180_22ee7debed9dad33b0a85e08c8cdfaa7.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(355, 154, '2024 - 2025', 'Phương Thức Kể Trong Sản Phẩm Truyền Thông', 'Trường Đại học Khoa học - Khoa Báo chí - Truyền thông - Môn Phương Thức Kể Trong Sản Phẩm Truyền Thông - 2024 - 2025', 'exam', 'static/exams/EY36TTKT_z6205695439381_74fbbfdec24ac33cfb2ba887a836be9c.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(356, 120, '2024 - 2025', 'Quản Lý Tài Nguyên Và Môi Trường Nước', 'Trường Đại học Khoa học - Khoa Địa lý - Địa chất - Môn Quản Lý Tài Nguyên Và Môi Trường Nước - 2024 - 2025', 'exam', 'static/exams/B7OFSU7E_z6205695533280_8d2f6f7754f6de5ad0b41cb3cba56375.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(357, 139, '2024 - 2025', 'Quan Hệ Công Chúng Và Giao Tiếp Công Vụ', 'Trường Đại học Khoa học - Khoa Lý luận chính trị - Môn Quan Hệ Công Chúng Và Giao Tiếp Công Vụ - 2024 - 2025', 'exam', 'static/exams/EY36TTKT_z6205695642026_dbb8c9b34bc9db56b2e2a0570c1c14cb.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(358, 118, '2024 - 2025', 'Môi Trường Trong Trắc Địa Và Đánh Giá Tác Động Môi Trường', 'Trường Đại học Khoa học - Khoa Địa lý - Địa chất - Môn Môi Trường Trong Trắc Địa Và Đánh Giá Tác Động Môi Trường - 2024 - 2025', 'exam', 'static/exams/YT360VTH_z6205695589701_c65f79c2f39070f288e303118e539eca.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(359, 113, '2024 - 2025', 'Sinh Lý Học Người Và Động Vật', 'Trường Đại học Khoa học - Khoa Sinh học - Môn Sinh Lý Học Người Và Động Vật - 2024 - 2025', 'exam', 'static/exams/FJC8P3MZ_z6205695651372_d585db5ea3976ed918241cd384292984.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(360, 63, '2024 - 2025', 'Đại Số Tuyến Tính 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Đại Số Tuyến Tính - 2024 - 2025', 'exam', 'static/exams/B7OFSU7E_z6205695615992_91af9a3f20e678e9f2634fcc3df1d937.jpg', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(361, 40, '2024 - 2025', 'Python', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Python - 2024 - 2025', 'exam', 'static/exams/EY36TTKT_3vv.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(362, 2, '2024 - 2025', 'Chính Trị Học Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Chính Trị Học Đại Cương - 2024 - 2025', 'exam', 'static/exams/EY36TTKT_471752404_1809474893198689_8805960458745095619_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(363, 54, '2024 - 2025', 'Cơ Sở Toán', 'Trường Đại học Khoa học - Khoa Toán - Môn Cơ Sở Toán - 2024 - 2025', 'exam', 'static/exams/EY36TTKT_80cf1b74-8c10-4b60-927f-12abf04bb96b.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(364, 40, '2024 - 2025', 'Python 1', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Python - 2024 - 2025', 'exam', 'static/exams/EY36TTKT_c1637e11-0040-49a8-a9f1-9558da680119.pdf', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(365, 69, '2024 - 2025', 'Hán Nôm Căn Bản', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Hán Nôm Căn Bản - 2024 - 2025', 'exam', 'static/exams/7270NNP5_e74be887-aa7d-4c4c-b415-26348e4c9089.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(366, 21, '2024 - 2025', 'Tâm Lý Học Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Tâm Lý Học Đại Cương - 2024 - 2025', 'exam', 'static/exams/7270NNP5_9c834cb2-2a32-487a-8b0c-efdc7117fb7a.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(367, 0, '2024 - 2025', 'Hệ Thống Chính Trị Các Nước Phương Đông', '', 'exam', 'static/exams/7270NNP5_c70ba7ba-bc6a-4934-9b08-13ae7699d978.jpg', '2025-02-20 03:34:30', '2025-02-20 05:04:26'),
(368, 76, '2024 - 2025', 'Tiếng Việt Thực Hành', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Tiếng Việt Thực Hành - 2024 - 2025', 'exam', 'static/exams/1Z72E7QP_dd371620-3c06-4110-bf1c-5610670e7f20.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(369, 129, '2024 - 2025', 'An Sinh Xã Hội Và Các Vấn Đề Xã Hội', 'Trường Đại học Khoa học - Khoa Xã hội học và Công tác xã hội - Môn An Sinh Xã Hội Và Các Vấn Đề Xã Hội - 2024 - 2025', 'exam', 'static/exams/0W7X4Y4Y_b6db67a7-dd8e-48f2-bcc2-d6c6ac2d57e7.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(370, 0, '2024 - 2025', 'Lịch Sử Đảng Việt Nam', '', 'exam', 'static/exams/N2G1RGNB_371a1cb2-01cd-4a47-9f23-816de4aeb62d.jpg', '2025-02-20 03:34:30', '2025-02-20 05:04:26'),
(371, 52, '2024 - 2025', 'Tâm Lý Học Báo Chí', 'Trường Đại học Khoa học - Khoa Báo chí - Truyền thông - Môn Tâm Lý Học Báo Chí - 2024 - 2025', 'exam', 'static/exams/H3KESOD2_c378360f-84f9-4563-b29a-59f4e704bf6f.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(372, 89, '2024 - 2025', 'Cơ Sở Truyền Thông Số', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Cơ Sở Truyền Thông Số - 2024 - 2025', 'exam', 'static/exams/AVDD8H0T_eadb8765-26ff-4d51-a689-bc08faf8157e.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(373, 12, '2024 - 2025', 'Vật Lý Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Vật Lý Đại Cương - 2024 - 2025', 'exam', 'static/exams/QH3X8X63_675f4a77-9649-4c37-8cd4-f23abee4830e.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(374, 14, '0', 'Đề Cương Xã Hội Học Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Xã Hội Học Đại Cương - 0', 'syllabus', 'static/exams/P0W7X4Y4_zx.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(375, 8, '2024 - 2025', 'Nhân Học Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Nhân Học Đại Cương - 2024 - 2025', 'exam', 'static/exams/Q3HTI6RQ_abe65e5c-138c-4453-902f-d2c88aec286c.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(376, 144, '2024 - 2025', 'Lịch Sử Triết Học Phương Đông', 'Trường Đại học Khoa học - Khoa Lý luận chính trị - Môn Lịch Sử Triết Học Phương Đông - 2024 - 2025', 'exam', 'static/exams/Q3HTI6RQ_z6214833398551_ae43548ce75986d667d240ffe38f834f.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(377, 0, '2024 - 2025', 'Lịch Sử Tư Tưởng Triết Học Việt Nam', '', 'exam', 'static/exams/ZL6JWGA0_z6214834691095_825e8f3c4f9563ab68f6059d573d2865.jpg', '2025-02-20 03:34:30', '2025-02-20 05:04:26'),
(378, 0, '0', 'Câu hỏi vấn đáp Phân Tích Thiết Kế Hệ Thống Thông Tin', '', 'syllabus', 'static/exams/KRQSDUBN_xxxxs.pdf', '2025-02-20 03:34:30', '2025-02-20 03:36:28'),
(379, 0, '2024 - 2025', 'Nhập Môn Lý Luận Văn Học', '', 'exam', 'static/exams/UMZCBYXB_7f6f9c5d-df3f-4559-b7fb-e1897c9acb73.jpg', '2025-02-20 03:34:30', '2025-02-20 05:04:26'),
(380, 4, '2024 - 2025', 'Lịch Sử Phương Đông Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Lịch Sử Phương Đông Đại Cương - 2024 - 2025', 'exam', 'static/exams/UMZCBYXB_17365781895641004314004635967878.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(381, 44, '2024 - 2025', 'Đồ Họa Máy Tính', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Đồ Họa Máy Tính - 2024 - 2025', 'exam', 'static/exams/UMZCBYXB_473044489_1357748741888339_7759714049877726958_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(382, 25, '2024 - 2025', 'Hướng Đối Tượng', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Hướng Đối Tượng - 2024 - 2025', 'exam', 'static/exams/UMZCBYXB_DeThi_638721958030398315_Deso1_Dot2.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(383, 111, '2024 - 2025', 'Lịch Sử Kiến Trúc Thế Giới', 'Trường Đại học Khoa học - Khoa Kiến trúc - Môn Lịch Sử Kiến Trúc Thế Giới - 2024 - 2025', 'exam', 'static/exams/G8JMFO5Z_z6218698677776_750ce9c053b0a9ee1248f9541cf18047.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(384, 12, '2024 - 2025', 'Vật Lý Đại Cương 2', 'Trường Đại học Khoa học - Môn học đại cương - Môn Vật Lý Đại Cương - 2024 - 2025', 'exam', 'static/exams/UMZCBYXB_z6218698107509_bb66fe8568b5ba2c7223bed6d25b772c.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(385, 141, '2024 - 2025', 'Quản Trị Học', 'Trường Đại học Khoa học - Khoa Lý luận chính trị - Môn Quản Trị Học - 2024 - 2025', 'exam', 'static/exams/UMZCBYXB_z6218698394614_845f7165a49a3cb6288ed1a78fc0976c.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(386, 125, '2024 - 2025', 'Tin Học Trong Trắc Địa', 'Trường Đại học Khoa học - Khoa Địa lý - Địa chất - Môn Tin Học Trong Trắc Địa - 2024 - 2025', 'exam', 'static/exams/JTJLQH2G_z6218698143715_aecd40e73422b5f2aef10f64427e418b.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(387, 28, '2024 - 2025', 'Kiến Trúc Máy Tính', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Kiến Trúc Máy Tính - 2024 - 2025', 'exam', 'static/exams/G8JMFO5Z_z6218699043170_499e0aefd3c745ecbd9e2cf6bbab277d.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(388, 61, '2024 - 2025', 'Toán Rời Rạc 1', 'Trường Đại học Khoa học - Khoa Toán - Môn Toán Rời Rạc - 2024 - 2025', 'exam', 'static/exams/EUS8MIBL_b4128a90-9e98-4b64-a26f-9593297c295c.pdf', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(389, 6, '2024 - 2025', 'Môi Trường Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Môi Trường Đại Cương - 2024 - 2025', 'exam', 'static/exams/06KGUJ4R_472931304_546333748372676_5186129248367504148_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(390, 55, '2024 - 2025', 'Giải Tích', 'Trường Đại học Khoa học - Khoa Toán - Môn Giải Tích - 2024 - 2025', 'exam', 'static/exams/CUJPJZLQ_z6226439844712_6a3f43616b30bfe9b8fecee7b958b0c1.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(391, 133, '2024 - 2025', 'Yếu Tố Văn Hóa Trong Thực Hành Công Tác Xã Hội', 'Trường Đại học Khoa học - Khoa Xã hội học và Công tác xã hội - Môn Yếu Tố Văn Hóa Trong Thực Hành Công Tác Xã Hội - 2024 - 2025', 'exam', 'static/exams/0SIPMESW_z6226439708589_e2c10d29d8c294adab58939951f608fe.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(392, 73, '2024 - 2025', 'Tiến Trình Văn Học', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Tiến Trình Văn Học - 2024 - 2025', 'exam', 'static/exams/C0BOP9TM_eec59651-8494-49a5-96a4-844189862519.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(393, 143, '2024 - 2025', 'Lịch Sử Triết Học Phương Tây Cổ Trung Đại', 'Trường Đại học Khoa học - Khoa Lý luận chính trị - Môn Lịch Sử Triết Học Phương Tây Cổ Trung Đại - 2024 - 2025', 'exam', 'static/exams/9WTRL5RF_z6229740276454_2e1ded8bbfa069e5d5005a1804df1535.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(394, 157, '2024 - 2025', 'Phương Pháp Luận Nghiên Cứu Khoa Học', 'Trường Đại học Khoa học - Khoa Xã hội học và Công tác xã hội - Môn Phương Pháp Luận Nghiên Cứu Khoa Học - 2024 - 2025', 'exam', 'static/exams/ZDO1NOUC_a6e1760d-03c1-423b-823f-9842e22cebc5.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(395, 63, '2024 - 2025', 'Đại Số Tuyến Tính Nâng Cao', 'Trường Đại học Khoa học - Khoa Toán - Môn Đại Số Tuyến Tính - 2024 - 2025', 'exam', 'static/exams/W3QUZUKP_fe1a5e61-6ca5-4382-8896-cf6adacf0a6a.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(396, 0, '0', 'Slide Thuyết Trình Kỹ Năng Mềm - Tham Khảo', '', 'syllabus', 'static/exams/IZ904E1M_knm.pptx', '2025-02-20 03:34:30', '2025-02-20 03:36:28'),
(397, 71, '2024 - 2025', 'Ngữ Dụng Học', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Ngữ Dụng Học - 2024 - 2025', 'exam', 'static/exams/IZ904E1M_7ab139aa-e1e0-4a05-8f46-5514a459f448.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(398, 156, '2024 - 2025', 'Lịch Sử Văn Minh Thế Giới', 'Trường Đại học Khoa học - Khoa Lịch sử - Môn Lịch Sử Văn Minh Thế Giới - 2024 - 2025', 'exam', 'static/exams/K72VNJZ0_3bbc5c9a-df44-431b-99d6-bc066669db00.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(399, 54, '0', 'Ngân hàng câu hỏi Cơ Sở Toán', 'Trường Đại học Khoa học - Khoa Toán - Môn Cơ Sở Toán - 0', 'syllabus', 'static/exams/9XFYPXPE_II_III_I_V_merged.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(400, 63, '0', 'Ngân hàng câu hỏi Đại Số Tuyến Tính', 'Trường Đại học Khoa học - Khoa Toán - Môn Đại Số Tuyến Tính - 0', 'syllabus', 'static/exams/9XFYPXPE_NganHang_DSTT_2015-1.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(401, 0, '0', 'Slide Thuyết Trình Kỹ Năng Mềm - Chủ đề Sinh viên đi làm thêm', '', 'syllabus', 'static/exams/RMI5ZYDX_Video_20250116_171737_0000.pptx', '2025-02-20 03:34:30', '2025-02-20 03:36:28'),
(402, 0, '0', 'Báo cáo đồ án Truyền Thông Số 1', '', 'syllabus', 'static/exams/IMHI693C_tts.docx', '2025-02-20 03:34:30', '2025-02-20 03:36:28'),
(403, 0, '0', 'Tiểu Luận Phân Tích Hình Thức Truyền Thông LIVESTREAM - Học phần Truyền thông tương tác', '', 'syllabus', 'static/exams/G98RLR7M_tieuluan.pdf', '2025-02-20 03:34:30', '2025-02-20 03:36:28');
INSERT INTO `documents` (`id`, `subject_id`, `year`, `file_name`, `file_info`, `document_type`, `file_path`, `created_at`, `updated_at`) VALUES
(404, 7, '2024 - 2025', 'Mỹ Học Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Mỹ Học Đại Cương - 2024 - 2025', 'exam', 'static/exams/5XD2W3Z4_ada1070e-3ee8-4484-a4e5-26689bcb3650.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(405, 43, '2024 - 2025', 'Trí Tuệ Nhân Tạo', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Trí Tuệ Nhân Tạo - 2024 - 2025', 'exam', 'static/exams/5XD2W3Z4_d577e99c-bb2c-4eee-a9f4-60f6539af072.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(406, 153, '2024 - 2025', 'Quản Lý An Toàn Nhiệt, Điện và Thiết Bị', 'Trường Đại học Khoa học - Khoa Điện, Điện tử và Công nghệ vật liêu - Môn Quản Lý An Toàn Nhiệt, Điện và Thiết Bị - 2024 - 2025', 'exam', 'static/exams/DSTBAKOM_9ff78933-46f8-4050-872e-ab94ea7d0426.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(407, 14, '2024 - 2025', 'Xã Hội Học Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Xã Hội Học Đại Cương - 2024 - 2025', 'exam', 'static/exams/5XD2W3Z4_d441f02e-2b69-4384-83c5-6720be4dd809.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(408, 15, '2024 - 2025', 'Đại Cương Chính Sách Công', 'Trường Đại học Khoa học - Môn học đại cương - Môn Đại Cương Chính Sách Công - 2024 - 2025', 'exam', 'static/exams/DSTBAKOM_4feca176-1f9b-4a53-a41f-22a810f2e748.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(409, 36, '2024 - 2025', 'Nhập Môn Cơ Sở Dữ Liệu', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nhập Môn Cơ Sở Dữ Liệu - 2024 - 2025', 'exam', 'static/exams/8X2O6JBZ_472422523_1343232453357093_2016452883896491049_.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(410, 138, '2024 - 2025', 'Luật Hành Chính', 'Trường Đại học Khoa học - Khoa Lý luận chính trị - Môn Luật Hành Chính - 2024 - 2025', 'exam', 'static/exams/YYE4Q912_472706570_1360188611821155_2175477454239689331_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(411, 151, '2024 - 2025', 'Địa Lý Du Lịch Việt Nam', 'Trường Đại học Khoa học - Khoa Lịch sử - Môn Địa Lý Du Lịch Việt Nam - 2024 - 2025', 'exam', 'static/exams/YYE4Q912_473284150_599186609502144_5742353869551729246_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(412, 149, '0', 'Câu hỏi ôn tập một số vấn đề về Đài Loan', 'Trường Đại học Khoa học - Khoa Lịch sử - Môn Một Số Vấn Đề Về Đài Loan - 0', 'syllabus', 'static/exams/2XSEWB95_zxccc.docx', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(413, 148, '0', 'CÂU HỎI ÔN TẬP MÔN MỘT SỐ VẤN ĐỀ VỀ LỊCH SỬ TRUNG QUỐC', 'Trường Đại học Khoa học - Khoa Lịch sử - Môn Một Số Vấn Đề Về Lịch Sử Trung Quốc - 0', 'syllabus', 'static/exams/NLG2VOTN_tq.docx', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(414, 18, '0', 'Đề cương học phần Tư Tưởng HCM', 'Trường Đại học Khoa học - Môn học đại cương - Môn Tư Tưởng HCM - 0', 'syllabus', 'static/exams/NLG2VOTN_zxxww.docx', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(415, 74, '2024 - 2025', 'Tiếng Trung Căn Bản 1', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Tiếng Trung Căn Bản 1 - 2024 - 2025', 'exam', 'static/exams/NLG2VOTN_471194316_617500800767518_1926404279347776591_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(416, 75, '2024 - 2025', 'Tiếng Trung Căn Bản 2', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Tiếng Trung Căn Bản 2 - 2024 - 2025', 'exam', 'static/exams/2XSEWB95_472843950_1647487885975020_485166704496893959_n.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(417, 148, '2024 - 2025', 'Một Số Vấn Đề Về Lịch Sử Trung Quốc', 'Trường Đại học Khoa học - Khoa Lịch sử - Môn Một Số Vấn Đề Về Lịch Sử Trung Quốc - 2024 - 2025', 'exam', 'static/exams/T6C07Q3S_473133974_587556240853136_2188398439430056314_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(418, 150, '2024 - 2025', 'Nhập Môn Nghiên Cứu Trung Quốc', 'Trường Đại học Khoa học - Khoa Lịch sử - Môn Nhập Môn Nghiên Cứu Trung Quốc - 2024 - 2025', 'exam', 'static/exams/T6C07Q3S_474234981_1131471598681099_330056146899898597_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(419, 149, '2024 - 2025', 'Một Số Vấn Đề Về Đài Loan', 'Trường Đại học Khoa học - Khoa Lịch sử - Môn Một Số Vấn Đề Về Đài Loan - 2024 - 2025', 'exam', 'static/exams/HKKNTKFX_473380720_2547986098730751_1321894792774812090_n.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(420, 37, '2024 - 2025', 'Nhập Môn Lập Trình 1', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Nhập Môn Lập Trình - 2024 - 2025', 'exam', 'static/exams/9ZA5LZWB_main.pdf', '2025-02-20 03:34:30', '2025-02-20 11:44:58'),
(421, 50, '0', 'Đề cương Sáng Tạo Nội Dung Truyền thông', 'Trường Đại học Khoa học - Khoa Báo chí - Truyền thông - Môn Sáng Tạo Nội Dung Truyền Thông - 0', 'syllabus', 'static/exams/TR2BKEOJ_sangtaonoidungtruyenthong.docx', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(422, 7, '0', 'Đề cương Mỹ Học Đại Cương', 'Trường Đại học Khoa học - Môn học đại cương - Môn Mỹ Học Đại Cương - 0', 'syllabus', 'static/exams/J38NUWWI_myhocdaicuong.docx', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(423, 157, '0', 'Đề Cương Phương Pháp Luận Nghiên Cứu Khoa Học', 'Trường Đại học Khoa học - Khoa Xã hội học và Công tác xã hội - Môn Phương Pháp Luận Nghiên Cứu Khoa Học - 0', 'syllabus', 'static/exams/29V1XIE3_pplnckh.docx', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(424, 0, '0', 'Hướng Dẫn Ôn Tập Triết Học Cổ Trung Đại', '', 'syllabus', 'static/exams/29V1XIE3_vc.docx', '2025-02-20 03:34:30', '2025-02-20 03:36:28'),
(425, 0, '0', 'Hướng Dẫn Ôn Tập Lịch Sử Tư Tưởng Chính Trị Và Quản Lý', '', 'syllabus', 'static/exams/9SZQC2Z6_lpoo.docx', '2025-02-20 03:34:30', '2025-02-20 03:36:28'),
(426, 78, '2024 - 2025', 'Tác Phẩm Và Thể Loại Văn Học', 'Trường Đại học Khoa học - Khoa Ngữ văn - Môn Tác Phẩm Và Thể Loại Văn Học - 2024 - 2025', 'exam', 'static/exams/88OUT91O_ad9eccd3-9daf-4467-9801-01e711cd4a36.jpg', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(427, 32, '0', 'Bộ Đề Thi Vấn Đáp Lý Thuyết Đồ Họa', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Lý Thuyết Đồ Họa - 0', 'syllabus', 'static/exams/O6PRT1QK_bo-de-thi-van-dap-ltdh-2018.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(428, 0, '0', 'Lý Thuyết Kiểm Định Phần Mềm', '', 'syllabus', 'static/exams/O6PRT1QK_on-tap-kiem-inh-phan-mem-on-tap-kdpm.pdf', '2025-02-20 03:34:30', '2025-02-20 03:36:28'),
(429, 0, '0', 'Đề Cương Sinh Đại Cương', '', 'syllabus', 'static/exams/QY1R1ORX_de-cuong-sinh-dai-cuong.pdf', '2025-02-20 03:34:30', '2025-02-20 03:36:28'),
(430, 29, '0', 'Kỹ nghệ phần mềm - Đề tài QUẢN LÍ MƯỢN TRẢ SÁCH THƯ VIỆN Ở TRƯỜNG ĐẠI HỌC KHOA HỌC', 'Trường Đại học Khoa học - Khoa Công nghệ Thông tin - Môn Kỹ Nghệ Phần Mềm - 0', 'syllabus', 'static/exams/O6PRT1QK_123doc-quan-ly-muon-tra-sach-o-thu-vien.pdf', '2025-02-20 03:34:30', '2025-02-20 05:17:45'),
(431, 0, '0', 'Mạng không dây và di động - Đề tài Thiết kế mạng WIRELESS', '', 'syllabus', 'static/exams/QY1R1ORX_mang-khong-day-va-di-dong.pdf', '2025-02-20 03:34:30', '2025-02-20 03:36:28');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `faculties`
--

CREATE TABLE `faculties` (
  `id` int(11) NOT NULL,
  `school_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `faculties`
--

INSERT INTO `faculties` (`id`, `school_id`, `name`) VALUES
(2, 1, 'Khoa Công nghệ Thông tin'),
(3, 1, 'Khoa Toán'),
(4, 1, 'Khoa Điện, Điện tử và Công nghệ vật liêu'),
(5, 1, 'Khoa Hóa học'),
(6, 1, 'Khoa Sinh học'),
(7, 1, 'Khoa Địa lý - Địa chất'),
(8, 1, 'Khoa Môi trường'),
(9, 1, 'Khoa Kiến trúc'),
(10, 1, 'Khoa Ngữ văn'),
(11, 1, 'Khoa Lịch sử'),
(12, 1, 'Khoa Lý luận chính trị'),
(13, 1, 'Khoa Báo chí - Truyền thông'),
(14, 1, 'Khoa Xã hội học và Công tác xã hội'),
(15, 2, 'Khoa Ngữ Văn'),
(16, 2, 'Khoa Lịch Sử'),
(17, 2, 'Khoa Địa lý'),
(18, 2, 'Khoa Toán học'),
(19, 2, 'Khoa Vật lý'),
(20, 2, 'Khoa Hóa học'),
(21, 2, 'Khoa Sinh học'),
(22, 2, 'Khoa Tin học'),
(23, 2, 'Khoa Giáo dục Tiểu học'),
(24, 2, 'Khoa Giáo dục Chính trị'),
(25, 2, 'Khoa Giáo dục Mầm non'),
(26, 2, 'Khoa Tâm lý và Giáo dục '),
(27, 2, 'Môn học đại cương'),
(28, 1, 'Môn học đại cương');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `schools`
--

CREATE TABLE `schools` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `schools`
--

INSERT INTO `schools` (`id`, `name`) VALUES
(1, 'Trường Đại học Khoa học'),
(2, 'Trường Đại học Sư phạm Huế');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `subjects`
--

CREATE TABLE `subjects` (
  `id` int(11) NOT NULL,
  `faculty_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `subjects`
--

INSERT INTO `subjects` (`id`, `faculty_id`, `name`) VALUES
(2, 28, 'Chính Trị Học Đại Cương'),
(3, 28, 'Hóa Học Đại Cương'),
(4, 28, 'Lịch Sử Phương Đông Đại Cương'),
(5, 28, 'Lịch Sử Việt Nam Đại Cương'),
(6, 28, 'Môi Trường Đại Cương'),
(7, 28, 'Mỹ Học Đại Cương'),
(8, 28, 'Nhân Học Đại Cương'),
(9, 28, 'Pháp Luật Việt Nam Đại Cương'),
(10, 28, 'Tôn Giáo Học Đại Cương'),
(11, 28, 'Văn Hóa Việt Nam Đại Cương'),
(12, 28, 'Vật Lý Đại Cương'),
(13, 28, 'Vật Lý Đại Cương 2'),
(14, 28, 'Xã Hội Học Đại Cương'),
(15, 28, 'Đại Cương Chính Sách Công'),
(16, 28, 'Chủ Nghĩa Xã Hội Khoa Học'),
(17, 28, 'Lịch Sử Đảng Cộng Sản Việt Nam'),
(18, 28, 'Tư Tưởng HCM'),
(19, 28, 'Kinh Tế Chính Trị Mác'),
(20, 28, 'Triết Học Mác'),
(21, 28, 'Tâm Lý Học Đại Cương'),
(22, 2, 'Các Hệ Quản Trị CSDL'),
(23, 2, 'Công Nghệ Phần Mềm'),
(24, 2, 'Font End'),
(25, 2, 'Hướng Đối Tượng'),
(26, 2, 'Java Cơ Bản'),
(27, 2, 'Java Nâng Cao'),
(28, 2, 'Kiến Trúc Máy Tính'),
(29, 2, 'Kỹ Nghệ Phần Mềm'),
(30, 2, 'Kỹ Thuật Lập Trình'),
(31, 2, 'Lập Trình Nâng Cao'),
(32, 2, 'Lý Thuyết Đồ Họa'),
(33, 2, 'Mô Hình Hóa UML'),
(34, 2, 'Mạng Máy Tính'),
(35, 2, 'Nguyên Lí Hệ Điều Hành'),
(36, 2, 'Nhập Môn Cơ Sở Dữ Liệu'),
(37, 2, 'Nhập Môn Lập Trình'),
(38, 2, 'Nhập Môn Trí Tuệ Nhân Tạo'),
(39, 2, 'Phân Tích Hệ Thống Thông Tin'),
(40, 2, 'Python'),
(41, 2, 'Thiết Kế Cơ Sở Dữ Liệu'),
(42, 2, 'Thiết Kế Đồ Hoạ Ứng Dụng'),
(43, 2, 'Trí Tuệ Nhân Tạo'),
(44, 2, 'Đồ Họa Máy Tính'),
(45, 2, 'SQL'),
(46, 13, 'Báo In'),
(47, 13, 'Các Phương Tiện Truyền Thông Mới'),
(48, 13, 'Lịch Sử Báo Chí Việt Nam'),
(49, 13, 'Quản Trị Truyền Thông Trong Khủng Hoảng'),
(50, 13, 'Sáng Tạo Nội Dung Truyền Thông'),
(51, 13, 'Truyền Thông Marketing Tích Hợp'),
(52, 13, 'Tâm Lý Học Báo Chí'),
(53, 13, 'Xã Hội Học Báo Chí'),
(54, 3, 'Cơ Sở Toán'),
(55, 3, 'Giải Tích'),
(56, 3, 'Giải Tích Nâng Cao'),
(57, 3, 'Phương Pháp Tính'),
(58, 3, 'Phép Tính Tích Phân Và Hàm Một Biến'),
(59, 3, 'Phép Tính Tích Phân Và Hàm Nhiều Biến'),
(60, 3, 'Phương Trình Vi Phân'),
(61, 3, 'Toán Rời Rạc'),
(62, 3, 'Xác Xuất Thống Kê'),
(63, 3, 'Đại Số Tuyến Tính'),
(64, 3, 'Đại Số Tuyến Tính Nâng Cao'),
(65, 3, 'Đại Số Tuyến Tính Và Hình Học Giải Tích'),
(66, 3, 'Toán Chuyên Nghành'),
(67, 10, 'Các Hướng Tiếp Cận Tác Phẩm Văn Học Chương Trình Phổ Thông'),
(68, 10, 'Cơ Sở Việt Ngữ Học'),
(69, 10, 'Hán Nôm Căn Bản'),
(70, 10, 'Ngôn Ngữ Học'),
(71, 10, 'Ngữ Dụng Học'),
(72, 10, 'Nhập Môn Lí Luận Văn Học'),
(73, 10, 'Tiến Trình Văn Học'),
(74, 10, 'Tiếng Trung Căn Bản 1'),
(75, 10, 'Tiếng Trung Căn Bản 2'),
(76, 10, 'Tiếng Việt Thực Hành'),
(77, 10, 'Tiếp Nhận Văn Học'),
(78, 10, 'Tác Phẩm Và Thể Loại Văn Học'),
(79, 10, 'Tổng Quan Văn Học Phương Đông'),
(80, 10, 'Văn Hóa Huế'),
(81, 10, 'Văn Hóa Và Văn Học Ấn Độ - Đông Nam Á'),
(82, 10, 'Văn Học Dân Gian'),
(83, 10, 'Văn Học Việt Nam Hiện Đại'),
(84, 10, 'Tổng Quan Văn Học Phương Tây'),
(85, 4, 'Anh Văn Chuyên Ngành'),
(86, 4, 'Cơ Sở Kỹ Thuật Chuyển Mạch'),
(87, 4, 'Cơ Sở Kỹ Thuật Truyền Số Liệu'),
(88, 4, 'Cơ Sở Lí Thuyết Thông Tin'),
(89, 4, 'Cơ Sở Truyền Thông Số'),
(90, 4, 'Cấu Kiện Điện Tử - Quang Điện Tử'),
(91, 4, 'Kỹ Thuật Mạch Điện Tử'),
(92, 4, 'Kỹ Thuật Siêu Cao Tần'),
(93, 4, 'Kỹ Thuật Số'),
(94, 4, 'Lý Thuyết Mạch'),
(95, 4, 'Lý Thuyết Truyền Sóng'),
(96, 4, 'Lý Thuyết Trường Điện Từ'),
(97, 4, 'Lý Thuyết Điều Khiển Tự Động'),
(98, 4, 'Nguồn Điện'),
(99, 4, 'Nghiên Cứu Và Xử Lí Thông Tin Định Lượng'),
(100, 4, 'Thông Tin Số'),
(101, 4, 'Vi Xử Lí'),
(102, 4, 'Xử Lý Số Tín Hiệu'),
(103, 4, 'Xử Lý Tín Hiệu Số 1'),
(104, 4, 'Điện Tử Ứng Dụng'),
(105, 4, 'Đo Lường Điện Tử Viễn Thông'),
(106, 4, 'Vi Xử Lý Và Vi Điều Khiển Trong Đo Lường Tự Động'),
(107, 9, 'Công Nghệ Chuyển Đổi Số Trong Kiến Trúc'),
(108, 9, 'Hình Học Họa Hình 1'),
(109, 9, 'Hình Học Họa Hình 2'),
(110, 9, 'Kỹ Thuật Xây Dựng Văn Bản'),
(111, 9, 'Lịch Sử Kiến Trúc Thế Giới'),
(112, 9, 'Quy Hoạch Xây Dựng Và Phát Triển Đô Thị'),
(113, 6, 'Sinh Lý Học Người Và Động Vật'),
(114, 2, 'Cấu Trúc Dữ Liệu và Thuật Toán'),
(115, 5, 'Hóa Học Phân Tích'),
(116, 8, 'Công Nghệ Môi Trường'),
(117, 8, 'Quản Lý Môi Trường Doanh Nghiệp'),
(118, 7, 'Môi Trường Trong Trắc Địa Và Đánh Giá Tác Động Môi Trường'),
(119, 7, 'Quản Lý Tài Nguyên Khoáng Sản Và Năng Lượng'),
(120, 7, 'Quản Lý Tài Nguyên Và Môi Trường Nước'),
(121, 7, 'Môi Trường Trong Trắc Địa Và Đánh Giá Tác Động Môi Trường'),
(122, 7, 'Quản Lý Tài Nguyên Khoáng Sản Và Năng Lượng'),
(123, 7, 'Quản Lý Tài Nguyên Và Môi Trường Nước'),
(124, 7, 'Quản Lý Tài Nguyên Và Môi Trường Đất'),
(125, 7, 'Tin Học Trong Trắc Địa'),
(126, 7, 'Đánh Giá Tác Động Môi Trường Và Môi Trường Chiến Lược'),
(127, 7, 'Địa Chất Việt Nam'),
(128, 7, 'Quản Lý Tài Nguyên Và Môi Trường Nước'),
(129, 14, 'An Sinh Xã Hội Và Các Vấn Đề Xã Hội'),
(130, 14, 'Hành Vi Lệch Chuẩn Và Các Vấn Đề Lứa Tuổi'),
(131, 14, 'Hành Vi Con Người Và Xã Hội'),
(132, 14, 'Nhập Môn Công Tác Xã Hội'),
(133, 14, 'Yếu Tố Văn Hóa Trong Thực Hành Công Tác Xã Hội'),
(134, 14, 'Các Vấn Đề Xã Hội Đương Đại'),
(135, 12, 'Cách Mạng Của Đảng Cộng Sản Việt Nam'),
(136, 12, 'Cơ Sở Khoa Học Của Con Đường Đi Lên Xã Hội Chủ Nghĩa Ở Việt Nam'),
(137, 12, 'Giới Thiệu Các Tác Phẩm Tiêu Biểu Của HCM'),
(138, 12, 'Luật Hành Chính'),
(139, 12, 'Quan Hệ Công Chúng Và Giao Tiếp Công Vụ'),
(140, 12, 'Luật Hành Chính'),
(141, 12, 'Quản Trị Học'),
(142, 12, 'Các Vấn Đề Xã Hội Đương Đại'),
(143, 12, 'Lịch Sử Triết Học Phương Tây Cổ Trung Đại'),
(144, 12, 'Lịch Sử Triết Học Phương Đông'),
(145, 12, 'Lịch Sử Tư Tưởng Chính Trị Và Quản Lí'),
(146, 12, 'Lịch Sử Tư Tưởng Phương Đông Và Việt Nam'),
(147, 11, 'Lịch Sử Việt Nam Cổ Đại Từ Nguyên Thủy Đến 1407'),
(148, 11, 'Một Số Vấn Đề Về Lịch Sử Trung Quốc'),
(149, 11, 'Một Số Vấn Đề Về Đài Loan'),
(150, 11, 'Nhập Môn Nghiên Cứu Trung Quốc'),
(151, 11, 'Địa Lý Du Lịch Việt Nam'),
(152, 11, 'Nhập Môn Khu Vực Học'),
(153, 4, 'Quản Lý An Toàn Nhiệt, Điện và Thiết Bị'),
(154, 13, 'Phương Thức Kể Trong Sản Phẩm Truyền Thông'),
(155, 12, 'Logic Học'),
(156, 11, 'Lịch Sử Văn Minh Thế Giới'),
(157, 14, 'Phương Pháp Luận Nghiên Cứu Khoa Học');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `departments_group`
--
ALTER TABLE `departments_group`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `documents`
--
ALTER TABLE `documents`
  ADD PRIMARY KEY (`id`),
  ADD KEY `subject_id` (`subject_id`);

--
-- Chỉ mục cho bảng `faculties`
--
ALTER TABLE `faculties`
  ADD PRIMARY KEY (`id`),
  ADD KEY `school_id` (`school_id`);

--
-- Chỉ mục cho bảng `schools`
--
ALTER TABLE `schools`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `subjects`
--
ALTER TABLE `subjects`
  ADD PRIMARY KEY (`id`),
  ADD KEY `faculty_id` (`faculty_id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `departments_group`
--
ALTER TABLE `departments_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT cho bảng `documents`
--
ALTER TABLE `documents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=432;

--
-- AUTO_INCREMENT cho bảng `faculties`
--
ALTER TABLE `faculties`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT cho bảng `schools`
--
ALTER TABLE `schools`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT cho bảng `subjects`
--
ALTER TABLE `subjects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=158;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
