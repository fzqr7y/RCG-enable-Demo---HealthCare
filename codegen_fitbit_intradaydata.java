// ORM class for table 'fitbit_intradaydata'
// WARNING: This class is AUTO-GENERATED. Modify at your own risk.
//
// Debug information:
// Generated date: Thu Sep 15 14:31:32 EDT 2016
// For connector: org.apache.sqoop.manager.PostgresqlManager
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapred.lib.db.DBWritable;
import com.cloudera.sqoop.lib.JdbcWritableBridge;
import com.cloudera.sqoop.lib.DelimiterSet;
import com.cloudera.sqoop.lib.FieldFormatter;
import com.cloudera.sqoop.lib.RecordParser;
import com.cloudera.sqoop.lib.BooleanParser;
import com.cloudera.sqoop.lib.BlobRef;
import com.cloudera.sqoop.lib.ClobRef;
import com.cloudera.sqoop.lib.LargeObjectLoader;
import com.cloudera.sqoop.lib.SqoopRecord;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.sql.Date;
import java.sql.Time;
import java.sql.Timestamp;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class codegen_fitbit_intradaydata extends SqoopRecord  implements DBWritable, Writable {
  private final int PROTOCOL_VERSION = 3;
  public int getClassFormatVersion() { return PROTOCOL_VERSION; }
  protected ResultSet __cur_result_set;
  private Integer id;
  public Integer get_id() {
    return id;
  }
  public void set_id(Integer id) {
    this.id = id;
  }
  public codegen_fitbit_intradaydata with_id(Integer id) {
    this.id = id;
    return this;
  }
  private String record_type;
  public String get_record_type() {
    return record_type;
  }
  public void set_record_type(String record_type) {
    this.record_type = record_type;
  }
  public codegen_fitbit_intradaydata with_record_type(String record_type) {
    this.record_type = record_type;
    return this;
  }
  private java.sql.Timestamp record_date;
  public java.sql.Timestamp get_record_date() {
    return record_date;
  }
  public void set_record_date(java.sql.Timestamp record_date) {
    this.record_date = record_date;
  }
  public codegen_fitbit_intradaydata with_record_date(java.sql.Timestamp record_date) {
    this.record_date = record_date;
    return this;
  }
  private java.math.BigDecimal value;
  public java.math.BigDecimal get_value() {
    return value;
  }
  public void set_value(java.math.BigDecimal value) {
    this.value = value;
  }
  public codegen_fitbit_intradaydata with_value(java.math.BigDecimal value) {
    this.value = value;
    return this;
  }
  private java.sql.Timestamp created_date;
  public java.sql.Timestamp get_created_date() {
    return created_date;
  }
  public void set_created_date(java.sql.Timestamp created_date) {
    this.created_date = created_date;
  }
  public codegen_fitbit_intradaydata with_created_date(java.sql.Timestamp created_date) {
    this.created_date = created_date;
    return this;
  }
  private java.sql.Timestamp modified_date;
  public java.sql.Timestamp get_modified_date() {
    return modified_date;
  }
  public void set_modified_date(java.sql.Timestamp modified_date) {
    this.modified_date = modified_date;
  }
  public codegen_fitbit_intradaydata with_modified_date(java.sql.Timestamp modified_date) {
    this.modified_date = modified_date;
    return this;
  }
  private String ext_value;
  public String get_ext_value() {
    return ext_value;
  }
  public void set_ext_value(String ext_value) {
    this.ext_value = ext_value;
  }
  public codegen_fitbit_intradaydata with_ext_value(String ext_value) {
    this.ext_value = ext_value;
    return this;
  }
  private Integer api_record_id;
  public Integer get_api_record_id() {
    return api_record_id;
  }
  public void set_api_record_id(Integer api_record_id) {
    this.api_record_id = api_record_id;
  }
  public codegen_fitbit_intradaydata with_api_record_id(Integer api_record_id) {
    this.api_record_id = api_record_id;
    return this;
  }
  private Integer created_by_id;
  public Integer get_created_by_id() {
    return created_by_id;
  }
  public void set_created_by_id(Integer created_by_id) {
    this.created_by_id = created_by_id;
  }
  public codegen_fitbit_intradaydata with_created_by_id(Integer created_by_id) {
    this.created_by_id = created_by_id;
    return this;
  }
  private Integer member_id;
  public Integer get_member_id() {
    return member_id;
  }
  public void set_member_id(Integer member_id) {
    this.member_id = member_id;
  }
  public codegen_fitbit_intradaydata with_member_id(Integer member_id) {
    this.member_id = member_id;
    return this;
  }
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (!(o instanceof codegen_fitbit_intradaydata)) {
      return false;
    }
    codegen_fitbit_intradaydata that = (codegen_fitbit_intradaydata) o;
    boolean equal = true;
    equal = equal && (this.id == null ? that.id == null : this.id.equals(that.id));
    equal = equal && (this.record_type == null ? that.record_type == null : this.record_type.equals(that.record_type));
    equal = equal && (this.record_date == null ? that.record_date == null : this.record_date.equals(that.record_date));
    equal = equal && (this.value == null ? that.value == null : this.value.equals(that.value));
    equal = equal && (this.created_date == null ? that.created_date == null : this.created_date.equals(that.created_date));
    equal = equal && (this.modified_date == null ? that.modified_date == null : this.modified_date.equals(that.modified_date));
    equal = equal && (this.ext_value == null ? that.ext_value == null : this.ext_value.equals(that.ext_value));
    equal = equal && (this.api_record_id == null ? that.api_record_id == null : this.api_record_id.equals(that.api_record_id));
    equal = equal && (this.created_by_id == null ? that.created_by_id == null : this.created_by_id.equals(that.created_by_id));
    equal = equal && (this.member_id == null ? that.member_id == null : this.member_id.equals(that.member_id));
    return equal;
  }
  public boolean equals0(Object o) {
    if (this == o) {
      return true;
    }
    if (!(o instanceof codegen_fitbit_intradaydata)) {
      return false;
    }
    codegen_fitbit_intradaydata that = (codegen_fitbit_intradaydata) o;
    boolean equal = true;
    equal = equal && (this.id == null ? that.id == null : this.id.equals(that.id));
    equal = equal && (this.record_type == null ? that.record_type == null : this.record_type.equals(that.record_type));
    equal = equal && (this.record_date == null ? that.record_date == null : this.record_date.equals(that.record_date));
    equal = equal && (this.value == null ? that.value == null : this.value.equals(that.value));
    equal = equal && (this.created_date == null ? that.created_date == null : this.created_date.equals(that.created_date));
    equal = equal && (this.modified_date == null ? that.modified_date == null : this.modified_date.equals(that.modified_date));
    equal = equal && (this.ext_value == null ? that.ext_value == null : this.ext_value.equals(that.ext_value));
    equal = equal && (this.api_record_id == null ? that.api_record_id == null : this.api_record_id.equals(that.api_record_id));
    equal = equal && (this.created_by_id == null ? that.created_by_id == null : this.created_by_id.equals(that.created_by_id));
    equal = equal && (this.member_id == null ? that.member_id == null : this.member_id.equals(that.member_id));
    return equal;
  }
  public void readFields(ResultSet __dbResults) throws SQLException {
    this.__cur_result_set = __dbResults;
    this.id = JdbcWritableBridge.readInteger(1, __dbResults);
    this.record_type = JdbcWritableBridge.readString(2, __dbResults);
    this.record_date = JdbcWritableBridge.readTimestamp(3, __dbResults);
    this.value = JdbcWritableBridge.readBigDecimal(4, __dbResults);
    this.created_date = JdbcWritableBridge.readTimestamp(5, __dbResults);
    this.modified_date = JdbcWritableBridge.readTimestamp(6, __dbResults);
    this.ext_value = JdbcWritableBridge.readString(7, __dbResults);
    this.api_record_id = JdbcWritableBridge.readInteger(8, __dbResults);
    this.created_by_id = JdbcWritableBridge.readInteger(9, __dbResults);
    this.member_id = JdbcWritableBridge.readInteger(10, __dbResults);
  }
  public void readFields0(ResultSet __dbResults) throws SQLException {
    this.id = JdbcWritableBridge.readInteger(1, __dbResults);
    this.record_type = JdbcWritableBridge.readString(2, __dbResults);
    this.record_date = JdbcWritableBridge.readTimestamp(3, __dbResults);
    this.value = JdbcWritableBridge.readBigDecimal(4, __dbResults);
    this.created_date = JdbcWritableBridge.readTimestamp(5, __dbResults);
    this.modified_date = JdbcWritableBridge.readTimestamp(6, __dbResults);
    this.ext_value = JdbcWritableBridge.readString(7, __dbResults);
    this.api_record_id = JdbcWritableBridge.readInteger(8, __dbResults);
    this.created_by_id = JdbcWritableBridge.readInteger(9, __dbResults);
    this.member_id = JdbcWritableBridge.readInteger(10, __dbResults);
  }
  public void loadLargeObjects(LargeObjectLoader __loader)
      throws SQLException, IOException, InterruptedException {
  }
  public void loadLargeObjects0(LargeObjectLoader __loader)
      throws SQLException, IOException, InterruptedException {
  }
  public void write(PreparedStatement __dbStmt) throws SQLException {
    write(__dbStmt, 0);
  }

  public int write(PreparedStatement __dbStmt, int __off) throws SQLException {
    JdbcWritableBridge.writeInteger(id, 1 + __off, 4, __dbStmt);
    JdbcWritableBridge.writeString(record_type, 2 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeTimestamp(record_date, 3 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeBigDecimal(value, 4 + __off, 2, __dbStmt);
    JdbcWritableBridge.writeTimestamp(created_date, 5 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeTimestamp(modified_date, 6 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeString(ext_value, 7 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeInteger(api_record_id, 8 + __off, 4, __dbStmt);
    JdbcWritableBridge.writeInteger(created_by_id, 9 + __off, 4, __dbStmt);
    JdbcWritableBridge.writeInteger(member_id, 10 + __off, 4, __dbStmt);
    return 10;
  }
  public void write0(PreparedStatement __dbStmt, int __off) throws SQLException {
    JdbcWritableBridge.writeInteger(id, 1 + __off, 4, __dbStmt);
    JdbcWritableBridge.writeString(record_type, 2 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeTimestamp(record_date, 3 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeBigDecimal(value, 4 + __off, 2, __dbStmt);
    JdbcWritableBridge.writeTimestamp(created_date, 5 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeTimestamp(modified_date, 6 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeString(ext_value, 7 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeInteger(api_record_id, 8 + __off, 4, __dbStmt);
    JdbcWritableBridge.writeInteger(created_by_id, 9 + __off, 4, __dbStmt);
    JdbcWritableBridge.writeInteger(member_id, 10 + __off, 4, __dbStmt);
  }
  public void readFields(DataInput __dataIn) throws IOException {
this.readFields0(__dataIn);  }
  public void readFields0(DataInput __dataIn) throws IOException {
    if (__dataIn.readBoolean()) { 
        this.id = null;
    } else {
    this.id = Integer.valueOf(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.record_type = null;
    } else {
    this.record_type = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.record_date = null;
    } else {
    this.record_date = new Timestamp(__dataIn.readLong());
    this.record_date.setNanos(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.value = null;
    } else {
    this.value = com.cloudera.sqoop.lib.BigDecimalSerializer.readFields(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.created_date = null;
    } else {
    this.created_date = new Timestamp(__dataIn.readLong());
    this.created_date.setNanos(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.modified_date = null;
    } else {
    this.modified_date = new Timestamp(__dataIn.readLong());
    this.modified_date.setNanos(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.ext_value = null;
    } else {
    this.ext_value = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.api_record_id = null;
    } else {
    this.api_record_id = Integer.valueOf(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.created_by_id = null;
    } else {
    this.created_by_id = Integer.valueOf(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.member_id = null;
    } else {
    this.member_id = Integer.valueOf(__dataIn.readInt());
    }
  }
  public void write(DataOutput __dataOut) throws IOException {
    if (null == this.id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeInt(this.id);
    }
    if (null == this.record_type) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, record_type);
    }
    if (null == this.record_date) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.record_date.getTime());
    __dataOut.writeInt(this.record_date.getNanos());
    }
    if (null == this.value) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    com.cloudera.sqoop.lib.BigDecimalSerializer.write(this.value, __dataOut);
    }
    if (null == this.created_date) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.created_date.getTime());
    __dataOut.writeInt(this.created_date.getNanos());
    }
    if (null == this.modified_date) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.modified_date.getTime());
    __dataOut.writeInt(this.modified_date.getNanos());
    }
    if (null == this.ext_value) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, ext_value);
    }
    if (null == this.api_record_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeInt(this.api_record_id);
    }
    if (null == this.created_by_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeInt(this.created_by_id);
    }
    if (null == this.member_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeInt(this.member_id);
    }
  }
  public void write0(DataOutput __dataOut) throws IOException {
    if (null == this.id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeInt(this.id);
    }
    if (null == this.record_type) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, record_type);
    }
    if (null == this.record_date) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.record_date.getTime());
    __dataOut.writeInt(this.record_date.getNanos());
    }
    if (null == this.value) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    com.cloudera.sqoop.lib.BigDecimalSerializer.write(this.value, __dataOut);
    }
    if (null == this.created_date) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.created_date.getTime());
    __dataOut.writeInt(this.created_date.getNanos());
    }
    if (null == this.modified_date) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.modified_date.getTime());
    __dataOut.writeInt(this.modified_date.getNanos());
    }
    if (null == this.ext_value) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, ext_value);
    }
    if (null == this.api_record_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeInt(this.api_record_id);
    }
    if (null == this.created_by_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeInt(this.created_by_id);
    }
    if (null == this.member_id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeInt(this.member_id);
    }
  }
  private static final DelimiterSet __outputDelimiters = new DelimiterSet((char) 1, (char) 10, (char) 0, (char) 0, false);
  public String toString() {
    return toString(__outputDelimiters, true);
  }
  public String toString(DelimiterSet delimiters) {
    return toString(delimiters, true);
  }
  public String toString(boolean useRecordDelim) {
    return toString(__outputDelimiters, useRecordDelim);
  }
  public String toString(DelimiterSet delimiters, boolean useRecordDelim) {
    StringBuilder __sb = new StringBuilder();
    char fieldDelim = delimiters.getFieldsTerminatedBy();
    __sb.append(FieldFormatter.escapeAndEnclose(id==null?"null":"" + id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(record_type==null?"null":record_type, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(record_date==null?"null":"" + record_date, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(value==null?"null":value.toPlainString(), delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(created_date==null?"null":"" + created_date, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(modified_date==null?"null":"" + modified_date, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(ext_value==null?"null":ext_value, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(api_record_id==null?"null":"" + api_record_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(created_by_id==null?"null":"" + created_by_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(member_id==null?"null":"" + member_id, delimiters));
    if (useRecordDelim) {
      __sb.append(delimiters.getLinesTerminatedBy());
    }
    return __sb.toString();
  }
  public void toString0(DelimiterSet delimiters, StringBuilder __sb, char fieldDelim) {
    __sb.append(FieldFormatter.escapeAndEnclose(id==null?"null":"" + id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(record_type==null?"null":record_type, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(record_date==null?"null":"" + record_date, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(value==null?"null":value.toPlainString(), delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(created_date==null?"null":"" + created_date, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(modified_date==null?"null":"" + modified_date, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(ext_value==null?"null":ext_value, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(api_record_id==null?"null":"" + api_record_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(created_by_id==null?"null":"" + created_by_id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(member_id==null?"null":"" + member_id, delimiters));
  }
  private static final DelimiterSet __inputDelimiters = new DelimiterSet((char) 1, (char) 10, (char) 0, (char) 0, false);
  private RecordParser __parser;
  public void parse(Text __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(CharSequence __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(byte [] __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(char [] __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(ByteBuffer __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(CharBuffer __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  private void __loadFromFields(List<String> fields) {
    Iterator<String> __it = fields.listIterator();
    String __cur_str = null;
    try {
    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.id = null; } else {
      this.id = Integer.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.record_type = null; } else {
      this.record_type = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.record_date = null; } else {
      this.record_date = java.sql.Timestamp.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.value = null; } else {
      this.value = new java.math.BigDecimal(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.created_date = null; } else {
      this.created_date = java.sql.Timestamp.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.modified_date = null; } else {
      this.modified_date = java.sql.Timestamp.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.ext_value = null; } else {
      this.ext_value = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.api_record_id = null; } else {
      this.api_record_id = Integer.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.created_by_id = null; } else {
      this.created_by_id = Integer.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.member_id = null; } else {
      this.member_id = Integer.valueOf(__cur_str);
    }

    } catch (RuntimeException e) {    throw new RuntimeException("Can't parse input data: '" + __cur_str + "'", e);    }  }

  private void __loadFromFields0(Iterator<String> __it) {
    String __cur_str = null;
    try {
    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.id = null; } else {
      this.id = Integer.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.record_type = null; } else {
      this.record_type = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.record_date = null; } else {
      this.record_date = java.sql.Timestamp.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.value = null; } else {
      this.value = new java.math.BigDecimal(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.created_date = null; } else {
      this.created_date = java.sql.Timestamp.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.modified_date = null; } else {
      this.modified_date = java.sql.Timestamp.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null")) { this.ext_value = null; } else {
      this.ext_value = __cur_str;
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.api_record_id = null; } else {
      this.api_record_id = Integer.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.created_by_id = null; } else {
      this.created_by_id = Integer.valueOf(__cur_str);
    }

    __cur_str = __it.next();
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.member_id = null; } else {
      this.member_id = Integer.valueOf(__cur_str);
    }

    } catch (RuntimeException e) {    throw new RuntimeException("Can't parse input data: '" + __cur_str + "'", e);    }  }

  public Object clone() throws CloneNotSupportedException {
    codegen_fitbit_intradaydata o = (codegen_fitbit_intradaydata) super.clone();
    o.record_date = (o.record_date != null) ? (java.sql.Timestamp) o.record_date.clone() : null;
    o.created_date = (o.created_date != null) ? (java.sql.Timestamp) o.created_date.clone() : null;
    o.modified_date = (o.modified_date != null) ? (java.sql.Timestamp) o.modified_date.clone() : null;
    return o;
  }

  public void clone0(codegen_fitbit_intradaydata o) throws CloneNotSupportedException {
    o.record_date = (o.record_date != null) ? (java.sql.Timestamp) o.record_date.clone() : null;
    o.created_date = (o.created_date != null) ? (java.sql.Timestamp) o.created_date.clone() : null;
    o.modified_date = (o.modified_date != null) ? (java.sql.Timestamp) o.modified_date.clone() : null;
  }

  public Map<String, Object> getFieldMap() {
    Map<String, Object> __sqoop$field_map = new TreeMap<String, Object>();
    __sqoop$field_map.put("id", this.id);
    __sqoop$field_map.put("record_type", this.record_type);
    __sqoop$field_map.put("record_date", this.record_date);
    __sqoop$field_map.put("value", this.value);
    __sqoop$field_map.put("created_date", this.created_date);
    __sqoop$field_map.put("modified_date", this.modified_date);
    __sqoop$field_map.put("ext_value", this.ext_value);
    __sqoop$field_map.put("api_record_id", this.api_record_id);
    __sqoop$field_map.put("created_by_id", this.created_by_id);
    __sqoop$field_map.put("member_id", this.member_id);
    return __sqoop$field_map;
  }

  public void getFieldMap0(Map<String, Object> __sqoop$field_map) {
    __sqoop$field_map.put("id", this.id);
    __sqoop$field_map.put("record_type", this.record_type);
    __sqoop$field_map.put("record_date", this.record_date);
    __sqoop$field_map.put("value", this.value);
    __sqoop$field_map.put("created_date", this.created_date);
    __sqoop$field_map.put("modified_date", this.modified_date);
    __sqoop$field_map.put("ext_value", this.ext_value);
    __sqoop$field_map.put("api_record_id", this.api_record_id);
    __sqoop$field_map.put("created_by_id", this.created_by_id);
    __sqoop$field_map.put("member_id", this.member_id);
  }

  public void setField(String __fieldName, Object __fieldVal) {
    if ("id".equals(__fieldName)) {
      this.id = (Integer) __fieldVal;
    }
    else    if ("record_type".equals(__fieldName)) {
      this.record_type = (String) __fieldVal;
    }
    else    if ("record_date".equals(__fieldName)) {
      this.record_date = (java.sql.Timestamp) __fieldVal;
    }
    else    if ("value".equals(__fieldName)) {
      this.value = (java.math.BigDecimal) __fieldVal;
    }
    else    if ("created_date".equals(__fieldName)) {
      this.created_date = (java.sql.Timestamp) __fieldVal;
    }
    else    if ("modified_date".equals(__fieldName)) {
      this.modified_date = (java.sql.Timestamp) __fieldVal;
    }
    else    if ("ext_value".equals(__fieldName)) {
      this.ext_value = (String) __fieldVal;
    }
    else    if ("api_record_id".equals(__fieldName)) {
      this.api_record_id = (Integer) __fieldVal;
    }
    else    if ("created_by_id".equals(__fieldName)) {
      this.created_by_id = (Integer) __fieldVal;
    }
    else    if ("member_id".equals(__fieldName)) {
      this.member_id = (Integer) __fieldVal;
    }
    else {
      throw new RuntimeException("No such field: " + __fieldName);
    }
  }
  public boolean setField0(String __fieldName, Object __fieldVal) {
    if ("id".equals(__fieldName)) {
      this.id = (Integer) __fieldVal;
      return true;
    }
    else    if ("record_type".equals(__fieldName)) {
      this.record_type = (String) __fieldVal;
      return true;
    }
    else    if ("record_date".equals(__fieldName)) {
      this.record_date = (java.sql.Timestamp) __fieldVal;
      return true;
    }
    else    if ("value".equals(__fieldName)) {
      this.value = (java.math.BigDecimal) __fieldVal;
      return true;
    }
    else    if ("created_date".equals(__fieldName)) {
      this.created_date = (java.sql.Timestamp) __fieldVal;
      return true;
    }
    else    if ("modified_date".equals(__fieldName)) {
      this.modified_date = (java.sql.Timestamp) __fieldVal;
      return true;
    }
    else    if ("ext_value".equals(__fieldName)) {
      this.ext_value = (String) __fieldVal;
      return true;
    }
    else    if ("api_record_id".equals(__fieldName)) {
      this.api_record_id = (Integer) __fieldVal;
      return true;
    }
    else    if ("created_by_id".equals(__fieldName)) {
      this.created_by_id = (Integer) __fieldVal;
      return true;
    }
    else    if ("member_id".equals(__fieldName)) {
      this.member_id = (Integer) __fieldVal;
      return true;
    }
    else {
      return false;    }
  }
}
