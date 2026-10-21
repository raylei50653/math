# profile1 完整 n-star 與必要支持的界線

原 profile1 有 `N_G(n)=(a,p,h,R,u4)`。同一原核心
`D=G−{b,p,h,R,x,y,r}` 因此滿足 `N_D(n)={a,u4}`，且 au4 是原邊。
這個完整 star 來自原嵌入及完整度數，沒有刪除額外鄰點的自由。

固定任一 D−n 的完整著色。如果 a、u4 的字面色不同，n 恰可用另外兩色。
在兩色間改 n，保留其餘全部原點，給兩個固定字面 D rim fibres 的雙射。
若全域正規化改變字面色名，須在全部私有點同時施行該置換。
例如原兩target的 n=1 改成3後，正規 state IDs 是66233、66242。
各對計數相等是原圖紙面結論；支持檢查本身不建立共同計數解。

固定任一互補 palette。若 a、u4 都不在 n 的 palette，n 在該 palette
的實際完整分量是單點。這個結論不能從「框接觸只有 n」反推；私有點
不存在於該分量，是原完整度數保證的。

原 orbit column 保存全部邊界分量的獨立 flips，每 palette 固定一個
anchor 除去全域內部翻色。對同 palette 的兩個框點，其相對 reference
row 的 XOR flips 向量相等，恰當它們在同一框接觸 block。
固定 anchor 不會把同 palette 的另一分量誤合併，因另一分量仍可獨立翻色。
因此程式可以安全排除「n 缺同 palette 原鄰點，卻同其他框點一個 block」的欄。
它只測這個必要條件，不聲稱由有限欄認證所有私有分量。

程式對兩組條件分別從原完整 family 開始：只加 au4 等色零值，以及再加
上述完整 star 必要欄限制。每輪先刪含零 fibre 的欄，再對每個 half-row 的
全部 incident columns 做非空檢查，最後同 state 三個 half-rows 共用零值。
這是原 `2Z=ΣX` 非負式的完整支持推論。
兩組各輪都相同，固定點均為38,647 states／133,271 columns；全部合法
n 改色仍在這個支持內。因此這項更明確的原 star 資訊沒有提供新零值。

normal與seed17 optimized逐字重播，獨立只讀審查確認XOR欄語義與原生成器
一致。三項內部污染及外部冒稱profile1已排除均拒絕。固定點存活不表示
計數錐可行，不表示來源實現；profiles0／1仍OPEN。
