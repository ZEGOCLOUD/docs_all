export function ImageList() {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      margin: '20px 0'
    }}>
      <div style={{
        flex: 1,
        textAlign: 'center',
        margin: '0 10px'
      }}>
        <img 
          src="https://zego-platform-growth.oss-cn-shanghai.aliyuncs.com/official-website/zego/activity/cloudMarket/20230920-190438.png"
          style={{
            height: '60px',
            width: 'auto',
            border: '1px solid #E5E7EB',
            borderRadius: '4px',
            padding: '4px'
          }}
        />
      </div>
      <div style={{
        flex: 1,
        textAlign: 'center',
        margin: '0 10px'
      }}>
        <img 
          src="https://zego-platform-growth.oss-cn-shanghai.aliyuncs.com/official-website/zego/activity/cloudMarket/guge-000.jpg"
          style={{
            height: '60px',
            width: 'auto',
            border: '1px solid #E5E7EB',
            borderRadius: '4px',
            padding: '4px'
          }}
        />
      </div>
      <div style={{
        flex: 1,
        textAlign: 'center',
        margin: '0 10px'
      }}>
        <img 
          src="https://zego-platform-growth.oss-cn-shanghai.aliyuncs.com/official-website/zego/activity/cloudMarket/yunshangqulv_icon.png"
          style={{
            height: '60px',
            width: 'auto',
            border: '1px solid #E5E7EB',
            borderRadius: '4px',
            padding: '4px'
          }}
        />
      </div>
    </div>
  );
}
export function SingleImage({ src }) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        margin: '20px 0'
      }}>
        <div style={{
          width: '33.33%',
          textAlign: 'left'
        }}>
          <img 
            src={src}
            style={{
              height: '60px',
              width: 'auto',
              border: '1px solid #E5E7EB',
              borderRadius: '4px',
              padding: '4px'
            }}
          />
        </div>
      </div>
    );
  }