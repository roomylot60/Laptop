### Encoder Class

- Encoder는 Transformer 기반의 인코더이며, 주어진 입력을 여러 개의 self-attention 레이어와 Feed-Forward Network (FFN) 레이어를 거쳐 변환합니다.
- 입력 시퀀스의 특징을 추출하고 변환하는 역할을 하며, 이를 위해 Multi-Head Attention과 FFN을 여러 층 쌓은 구조를 가집니다.

```python
# 클래스 정의
class Encoder(nn.Module):
    def __init__(self, hidden_channels, filter_channels, n_heads, n_layers, kernel_size=1, p_dropout=0., window_size=4, **kwargs):
        hidden_channels : 모델의 내부 차원 크기 (특징 벡터 크기)
        filter_channels : Feed-Forward Network(FFN)에서 중간 계층의 크기
        n_heads : Multi-Head Attention에서 사용할 헤드(head)의 개수
        n_layers : 인코더에 포함된 Transformer 블록 개수
        kernel_size : FFN에서 사용할 CNN의 커널 크기
        p_dropout : Dropout 비율
        window_size : 상대적 위치 정보(Relative Position Encoding)에서 사용할 윈도우 크기
```

#### 1. 가중치 및 레이어 초기화
```python
# 클래스 멤버 변수로 입력된 하이퍼파라미터들을 저장합니다.
super().__init__()
self.hidden_channels = hidden_channels
self.filter_channels = filter_channels
self.n_heads = n_heads
self.n_layers = n_layers
self.kernel_size = kernel_size
self.p_dropout = p_dropout
self.window_size = window_size
```

#### 2. 레이어 정의
```python
self.drop = nn.Dropout(p_dropout)
self.attn_layers = nn.ModuleList()
self.norm_layers_1 = nn.ModuleList()
self.ffn_layers = nn.ModuleList()
self.norm_layers_2 = nn.ModuleList()
```

- 여러 층을 쌓아야 하므로, ModuleList()를 사용해 리스트 형태로 레이어들을 정의합니다.
    - `self.attn_layers` : 여러 개의 Multi-Head Attention 레이어
    - `self.norm_layers_1` : Self-Attention 후 LayerNorm
    - `self.ffn_layers` : FFN 레이어 (MLP 구조)
    - `self.norm_layers_2` : FFN 후 LayerNorm

#### 3. Transformer 블록 생성
```python
for i in range(self.n_layers):
    self.attn_layers.append(MultiHeadAttention(hidden_channels, hidden_channels, n_heads, p_dropout=p_dropout, window_size=window_size))
    self.norm_layers_1.append(LayerNorm(hidden_channels))
    self.ffn_layers.append(FFN(hidden_channels, hidden_channels, filter_channels, kernel_size, p_dropout=p_dropout))
    self.norm_layers_2.append(LayerNorm(hidden_channels))
```

- n_layers 개수만큼 Transformer 블록을 쌓습니다.
- 각 블록은 `Multi-Head Attention` → `LayerNorm` → `FFN` → `LayerNorm` 순서로 구성됩니다.
- `MultiHeadAttention` 과 `FFN` 은 각각 다른 클래스에서 정의됨.

#### 4. forward() 함수
```python
# 입력 및 마스킹 처리
def forward(self, x, x_mask):
    attn_mask = x_mask.unsqueeze(2) * x_mask.unsqueeze(-1)
    x = x * x_mask
```

- `x`: 입력 텐서
- `x_mask`: 입력 마스크 (0은 패딩, 1은 유효한 토큰)
- `attn_mask`: 마스크를 3차원으로 확장 (unsqueeze(2), unsqueeze(-1)) `attn_mask = x_mask * x_mask^T` 를 계산하여 `Self-Attention` 시 패딩 토큰을 무시하도록 함
- `x = x * x_mask` : 패딩된 부분을 0으로 만들어 모델이 무시하도록 함

#### 5. Transformer 블록 연산
```python
# 각 층에서 다음과 같은 연산을 수행
for i in range(self.n_layers): # x는 (batch_size, seq_len, hidden_dim)의 tensor
    y = self.attn_layers[i](x, x, attn_mask)
    y = self.drop(y)
    x = self.norm_layers_1[i](x + y)

    y = self.ffn_layers[i](x, x_mask)
    y = self.drop(y)
    x = self.norm_layers_2[i](x + y)
```

- 각 블록은 *Multi-Head Attention (MHA)* → *Residual Connection* + *LayerNorm* → *Feed-Forward Network (FFN)* → *Residual Connection* + *LayerNorm* 순서로 연산됩니다.
    - Multi-Head Attention 연산 :
        (1) 입력 x를 Q, K, V로 변환하여 Self-Attention 수행
        (2) attn_mask를 사용하여 패딩 부분을 무시
        (3) 출력 y를 Dropout 적용
    - Residual Connection + Layer Normalization : x = LayerNorm(x + y) 로 업데이트
    - Feed-Forward Network (FFN) 연산 :
        (1) 입력을 1D 컨볼루션 기반 FFN에 통과
        (2) x_mask를 적용해 패딩된 부분을 유지
        (3) Dropout 적용 후 결과를 저장
    - Residual Connection + Layer Normalization : 최종적으로 x = LayerNorm(x + y) 로 업데이트

#### 6. 최종 출력
```python
x = x * x_mask
return x
```

패딩된 부분이 0이 되도록 마스크 적용 후 최종 출력 반환
정리
구조
Encoder는 n_layers 개의 Transformer 블록으로 이루어짐
각 블록은 Multi-Head Attention → LayerNorm → Feed-Forward Network → LayerNorm 구조
패딩을 고려하여 x_mask를 사용한 마스킹 처리
입력과 출력
입력: (batch_size, hidden_dim, sequence_length) 형태의 텐서
출력: 동일한 크기의 텐서, 각 토큰이 컨텍스트 정보를 포함한 벡터로 변환됨